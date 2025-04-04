SECRET_KEY = "dev"  # Set this to a secure value in production
DOMAIN_NAME = "127.0.0.1:5000"  # Set this to your domain in production, don't append a trailing slash
MONGO_URI = "mongodb://127.0.0.1:27017/users"
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "username"
MAIL_PASSWORD = "password"
OPENAI_API_KEY = "sk-something"  # main summarization API key
FTP_HOST = "0.0.0.0"
FTP_USER = "username"
FTP_PASSWORD = "password"
ADMIN_USER_EMAILS = ["email@email.com"]  # Users who will have access to the admin panel
API_NINJA_KEY = ""  # API key for API Ninja, Get it from https://api-ninjas.com/ required for surprise function in email
MISTRAL_API_KEY = (
    ""  # API key for Mistral AI, Get it from https://mistral.ai/ required for summaries
)
FORM_WEBHOOK = None
WRITER_WEBHOOK = None  # Webhook where we will get notified on a new application
CRON_JOB_WEBHOOK = None  # Webhook where we will get notified when running cron jobs
TURNSTILE_SITE_KEY = ""  # cloudflare Turnstile site key
TURNSTILE_SECRET_KEY = ""  # cloudflare Turnstile secret key
