import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
from pathlib import Path

# Charger les identifiants depuis un fichier .env
dotenv_path = Path('credentials.env')
load_dotenv(dotenv_path=dotenv_path)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.lmd.ipsl.fr")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # sécurise la connexion
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print("✅ Mail envoyé avec succès !")
    except Exception as e:
        print("❌ Erreur :", e)

# Exemple d'utilisation
# send_email(
#     "maximilien.wemaere@gmail.com",
#     "Test depuis mon adresse IPSL",
#     "Bonjour, ceci est un test d'envoi automatique depuis mon adresse institutionnelle."
# )




def send_email_with_attachment(to_email, subject, body, file_path):
    # Création du message
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    # Ajouter le texte
    msg.attach(MIMEText(body, "plain"))

    # Ajouter la pièce jointe
    if file_path:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(file_path)}",
        )
        msg.attach(part)

    # Connexion SMTP et envoi
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print("✅ Mail envoyé avec pièce jointe !")
    except Exception as e:
        print("❌ Erreur :", e)

# Exemple d'utilisation
send_email_with_attachment(
    "maximilien.wemaere@gmail.com",
    "Test avec PJ",
    "Bonjour, voici un test avec pièce jointe.",
    "send_mail_mg.py"  # chemin vers ton fichier
)
