import smtplib

def send_email(user, pwd, recipient, subject, body):

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as ex:
        print("failed to send mail")


usr = "botuserbox@gmail.com"
pwd = "b0td3mo0ne"
rcp = "jborelo@gmail.com"
subj = "PythnonEmailTests"
body = "asasasasa" \
       "ewrewrewrewr" \
       "wrewrewrewrew"

send_email(usr, pwd, rcp, subj, body)

print ("DONE")