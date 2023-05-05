import html
import random
from ftplib import FTP


def clean_html(html_string):
    return (
        html.escape(html_string, quote=False)
        .replace("<script>", "&lt;script&gt;")
        .replace("</script>", "&lt;/script&gt;")
        .replace("<style>", "&lt;style&gt;")
        .replace("</style>", "&lt;/style&gt;")
    )


allowed_file_types = lambda filename: "." in filename and filename.rsplit(".", 1)[
    1
].lower() in ["png", "jpg", "jpeg"]


def upload_file(file, filename, current_app):
    # TODO Convert the images to one format, so we can use the same extension in /portal

    if file.filename and allowed_file_types(file.filename):
        # Rename the file to the user_name
        file.filename = f"{filename}.jpg"
        # Connect to FTP server
        ftp = FTP(current_app.config["FTP_HOST"])
        ftp.login(
            user=current_app.config["FTP_USER"],
            passwd=current_app.config["FTP_PASSWORD"],
        )
        # Upload file to the directory htdocs/images
        if file.filename in ftp.nlst("htdocs"):
            ftp.delete(f"htdocs/{file.filename}")
        ftp.storbinary(f"STOR /htdocs/{file.filename}", file)
        # Close FTP connection
        ftp.quit()
        return True
    elif file.filename and not allowed_file_types(file.filename):
        return False


def format_html(text):
    # Replace '\n' with '<br>'
    text = text.replace("\n", "<br>")
    text = text.replace("\t", "")
    # Add styling to <code> tag
    text = text.replace(
        "<code>",
        '<code style="background-color: #f1f1f1; color: #0B36FA; padding: 2px 4px; border-radius: 4px; font-family: monospace;">',
    )
    text = text.replace("</code>", "</code>")
    return text


def random_language_greeting():
    json = {
            "english": "Good Morning",
            "spanish": "¡Buenos días",
            "chinese": "早上好！",
            "hindi": "शुभ प्रभात",
            "arabic": "صباح الخير",
            "portuguese": "Bom dia",
            "bengali": "শুভ সকাল",
            "russian": "Доброе утро",
            "japanese": "おはようございます！",
            "punjabi": "ਸ਼ੁਭ ਸਵੇਰ",
            "german": "Guten Morgen",
            "georgian": "დილა მშვიდობის",
            "korean": "안녕하세요",
            "french": "Bonjour",
            "turkish": "Günaydın",
            "italian": "Buongiorno",
            "urdu": "صبح بخیر",
            "polish": "Dzień dobry",
            "javanese": "Selamat pagi",
            "marathi": "शुभ प्रभात",
            "dutch": "Goedemorgen",
        }
    language, value = random.choice(list(json.items()))
    return language.capitalize(), value
