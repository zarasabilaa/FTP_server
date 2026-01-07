import os
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.ftp_controller import FTPController
from app.config import UPLOAD_FOLDER

main = Blueprint("main", __name__)

ftp_ctx = {"ftp": None, "home": None}


@main.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        try:
            ftp = FTPController()
            ftp.login(user, pwd)
            ftp_ctx["ftp"] = ftp
            ftp_ctx["home"] = ftp.pwd()
            return redirect(url_for("main.dashboard"))
        except:
            return render_template("login.html", error="Login FTP gagal")

    return render_template("login.html")


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    ftp = ftp_ctx.get("ftp")
    if not ftp:
        return redirect(url_for("main.login"))

    message = error = None

    # MENU 6: UPLOAD
    if "file" in request.files:
        file = request.files["file"]
        local_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(local_path)
        ftp.upload(local_path, file.filename)
        message = f"Upload berhasil: {file.filename}"

    return render_template(
        "dashboard.html",
        pwd=ftp.pwd(),
        items=ftp.list_items(),
        message=message,
        error=error,
    )


# 🔑 PINDAH DIREKTORI DENGAN KLIK
@main.route("/cd/<folder>")
def cd(folder):
    ftp_ctx["ftp"].cwd(folder)
    return redirect(url_for("main.dashboard"))


# KEMBALI KE HOME
@main.route("/home")
def home():
    ftp_ctx["ftp"].home(ftp_ctx["home"])
    return redirect(url_for("main.dashboard"))


# DOWNLOAD FILE
@main.route("/download/<filename>")
def download(filename):
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    ftp_ctx["ftp"].download(filename, local_path)
    return send_file(local_path, as_attachment=True)


# DELETE FILE
@main.route("/delete/<filename>")
def delete(filename):
    ftp_ctx["ftp"].delete(filename)
    return redirect(url_for("main.dashboard"))


@main.route("/logout")
def logout():
    ftp_ctx["ftp"].close()
    ftp_ctx["ftp"] = None
    return redirect(url_for("main.login"))
