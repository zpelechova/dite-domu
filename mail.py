from flask import request, url_for
from flask_login import current_user
import databaze
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

#tenhle mail odejde ve chvíli, kdy NR zadá email a heslo (registruje se) - odkaz na dotazník.
def email_dotaznik(email, id):
    #měl by být závod, na který auto přihlásil
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

# def email_o_nastupu_do_auta(uzivatel,id_zavod,id_jizdy):
# 	server = smtplib.SMTP('smtp.gmail.com',587)
# 	email = uzivatel.id
# 	zavod = db_funkce.zavod(id_zavod)
# 	ridic = db_funkce.posta_ridic(id_jizdy)
# 	nazev_zavodu = zavod.nazev
# 	datum = zavod.datum_zavodu.strftime('%d.%m.%Y')
# 	misto = zavod.misto_zavodu
# 	sofer = ridic.jmeno
# 	mobil = ridic.telefon
# 	email_ridice = ridic.email
# 	odjezd = ridic.misto_odjezdu
# 	datum_odj = ridic.datum_odjezdu.strftime('%d.%m.%Y')
# 	zprava = EmailMessage()
# 	zprava['Subject'] = "Jedete spolu!"
# 	zprava['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
# 	zprava['To'] = uzivatel.id
# 	zprava['Message-Id'] = make_msgid()
# 	text = f"""Ahoj!
# 	Právě jsi na bezcisobe.cz potvrdil/a, že chceš jet na {datum} {nazev_zavodu} {misto} s {sofer}. Odjizdite z {odjezd} v terminu {datum_odj}.
# 	Tady jsou potřebné kontakty  na řidiče:
#  	* telefon: {mobil}
#  	* mail: {email_ridice}
# 	Skvělý zážitek přeji!
# 	Ivka z Běžci Sobě"""
# 	zprava.set_content(text)
# 	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
# 	mail.ehlo()
# 	mail.starttls()
# 	mail.login('bezcisobe@gmail.com','behamespolu')
# 	mail.sendmail('bezcisobe@gmail.com',email, zprava.as_string())
# 	mail.close()

# #mail se odešle ve chvíli kdy někdo nastoupí do nabízeného auta
# def email_spolujizda_ridic(uzivatel,id_zavod,id_jizdy):
# 	server = smtplib.SMTP('smtp.gmail.com',587)
# 	ridic = db_funkce.email_ridic(id_jizdy)
# 	zavod = db_funkce.zavod(id_zavod)
# 	nazev_zavodu = zavod.nazev
# 	datum = zavod.datum_zavodu.strftime('%d.%m.%Y')
# 	misto = zavod.misto_zavodu
# 	jmeno_spolucestujiciho = uzivatel.jmeno #jmeno aktuálně prihlášeného uživatele, který potvrdil nástup do auta
# 	email_uzivatele = uzivatel.id #uzivatel.id aktuálně prihlášeného uživatele, který potvrdil nástup do auta
# 	mobil_uzivatele = uzivatel.telefon #telefon aktuálně přihlášeného uživatele, který potvrdil nástup do auta
# 	zprava = EmailMessage()
# 	zprava['Subject'] = "Jedete spolu!"
# 	zprava['From'] = Address('Běžci Sobě', 'bezcisobe', 'gmail.com')
# 	zprava['To'] = ridic.email
# 	zprava['Message-Id'] = make_msgid()
# 	text = f"""Ahoj!
# 	{jmeno_spolucestujiciho} si Tě právě na bezcisobe.cz vybral/a jako svého řidiče na {datum} {nazev_zavodu} {misto}.
# 	Tady jsou potřebné kontakty spolucestujícího:
# 	* telefon: {mobil_uzivatele}
# 	* mail: {email_uzivatele}
# 	Doladění detailů už je na vás:)
# 	Skvelý zážitek přeji!
# 	Ivka z Běžci Sobě"""
# 	zprava.set_content(text)
# 	mail = smtplib.SMTP(host='smtp.gmail.com',port=587)
# 	mail.ehlo()
# 	mail.starttls()
# 	mail.login('bezcisobe@gmail.com','behamespolu')
# 	mail.sendmail('bezcisobe@gmail.com',ridic.email, zprava.as_string())
# 	mail.close()