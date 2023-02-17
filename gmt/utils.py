import html
from ftplib import FTP


def clean_html(html_string):
    return (
        html.escape(html_string, quote=False)
        .replace("<script>", "&lt;script&gt;")
        .replace("</script>", "&lt;/script&gt;")
        .replace("<style>", "&lt;style&gt;")
        .replace("</style>", "&lt;/style&gt;")
    )


allowed_file_types = lambda filename: "." in filename and filename.rsplit(".", 1)[1].lower() in ["png", "jpg",
                                                                                                     "jpeg"]
def upload_file(file, filename, current_app):
    # TODO Convert the images to one format, so we can use the same extension in /portal

    if file.filename and allowed_file_types(file.filename):
        # Rename the file to the user_name
        file.filename = f"{filename}.jpg"
        # Connect to FTP server
        ftp = FTP(current_app.config["FTP_HOST"])
        ftp.login(user=current_app.config["FTP_USER"], passwd=current_app.config["FTP_PASSWORD"])
        # Upload file to the directory htdocs/images
        if file.filename in ftp.nlst("htdocs"):
            ftp.delete(f"htdocs/{file.filename}")
        ftp.storbinary(f"STOR /htdocs/{file.filename}", file)
        # Close FTP connection
        ftp.quit()
        return True
    elif file.filename and not allowed_file_types(file.filename):
        return False