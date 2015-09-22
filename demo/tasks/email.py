from flask_mail import Mail, Message


default_mail = """Bonjour {0},
Veuillez trouver ci-dessous votre mot de passe temporaire :
    {2}

Cordialement,
-- Mailer Daemon"""

default_subject = "Votre mot de passe ASILE"


class MailHandler:

    def init_app(self, app):
        app.config.setdefault('MAIL_DISABLED', False)
        if not app.config['MAIL_DISABLED']:
            self.mail = Mail(app)
        else:
            self.mail = None

    def send(self, body=None, recipient=None, subject=None):
        if self.mail:
            msg = Message(subject=subject, body=body)
            msg.add_recipient(recipient)
            return self.mail.send(msg)

    def record_messages(self, *args, **kwargs):
        if self.mail:
            return self.mail.record_messages(*args, **kwargs)

mail = MailHandler()
