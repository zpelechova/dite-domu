from flask import request, url_for
from flask_login import current_user
import databaze
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

#tenhle mail odejde ve chvíli, kdy NR zadá email a heslo (registruje se) - odkaz na dotazník.
def email_dotaznik(email, id):
    link = 'https://ditedomu.herokuapp.com/dotaznik/' + str(id)
    zprava = EmailMessage()
    zprava['Subject'] = "Pokračujte na dotazník"
    zprava['From'] = Address('Dítě Domů', 'ditedomu', 'gmail.com')
    zprava['To'] = email
    zprava['Message-Id'] = make_msgid()
    text = f"""Dobrý den, vítejte, vyplnte dotazník tady: {link}. """
    zprava.set_content(text)
    mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
    mail.ehlo()
    mail.starttls()
    mail.login('ditedomu@gmail.com','dite13062019domu')
    mail.sendmail('ditedomu@gmail.com',email, zprava.as_string())
    mail.close()
