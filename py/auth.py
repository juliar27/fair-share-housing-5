import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment


def auth_email(receiver_email, link):
    sender_email = "nobodyatmapfsh@gmail.com"
    password = "welovebob"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your mapFSH Account"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    html = """\
        <html>
          <body>
            <p>
               Please verify your mapFSH account: {{link}}
               <br><br>
               mapFSH
            </p>
          </body>
        </html>
        """

    # Turn these into plain/html MIMEText objects
    # part2 = MIMEText(html, "html")

    part2 = MIMEText(
        Environment().from_string(html).render(
            link=link
        ), "html"
    )

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def recovery_email(receiver_email, link):
    sender_email = "nobodyatmapfsh@gmail.com"
    password = "welovebob"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Recovery"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    html = """\
        <html>
          <body>
            <p>
               To change your mapFSH password, please use this link: {{link}}
               <br>
               <br>
               If you did not request to change your password, please contact the system administrators.
               <br><br>
               mapFSH
            </p>
          </body>
        </html>
        """

    # Turn these into plain/html MIMEText objects
    # part2 = MIMEText(html, "html")

    part2 = MIMEText(
        Environment().from_string(html).render(
            link=link
        ), "html"
    )

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
