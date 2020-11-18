import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment
from threading import Thread

class Server:
    def __init__(self):
        self._context = ssl.create_default_context()
        self._server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self._context)

    def sendEmail(self, subject, receiver_email, html, link):
        sender_email = "nobodyatmapfsh@gmail.com"
        password = "welovebob"

        self._server.login(sender_email, password)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        part2 = MIMEText(
            Environment().from_string(html).render(
                link=link
            ), "html"
        )

        message.attach(part2)

        self._server.sendmail(sender_email, receiver_email, message.as_string())

class EmailThreads (Thread):
    def __init__(self, server, receiver_email, html, subject, link):
        Thread.__init__(self)
        self._server = server
        self._receiver_email = receiver_email
        self._html = html
        self._subject =  subject
        self._link = link

    def run(self):
        self._server.sendEmail(self._subject, self._receiver_email, self._html, self._link)


def auth_email(receiver_email, link):
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

    server = Server()
    thread = EmailThreads(server, receiver_email, html, "Verify your mapFSH Account", link)
    thread.start()



def recovery_email(receiver_email, link):
    html = """\
        <html>
          <body>
            <p>
               Someone (hopefully you) has requested a password reset. To change your mapFSH password, please use this link: {{link}}
               <br>
               <br>
               If you don't wish to reset your password, disregard this email and no action will be taken.
               <br><br>
               mapFSH
            </p>
          </body>
        </html>
        """

    server = Server()
    thread = EmailThreads(server, receiver_email, html, "Reset your mapFSH Password", link)
    thread.start()
