from core.model_util import fields
from core.auth import generate_password
from core.model import UserDocument, UserDocumentSearcher, UserDocumentController
from sample.tasks.email import default_mail, mail, default_subject
from sample.roles import ROLES


class UserController(UserDocumentController):

    def set_password_and_email(self):
        from core.auth import encrypt_password
        clear_pwd = generate_password()
        self.document.password = encrypt_password(clear_pwd)
        # send email
        body = default_mail.format(name=self.document.email, password=clear_pwd)
        mail.send(subject=default_subject, recipient=self.document.email, body=body)


class UserSearcher(UserDocumentSearcher):
    FIELDS = ('email', 'role')


class User(UserDocument):
    meta = {'controller_cls': UserController, 'searcher_cls': UserSearcher}
    role = fields.StringField(choices=list(ROLES.keys()), null=True)
    permissions = fields.ListField(fields.StringField(), default=list)
    lastname = fields.StringField(max_length=255)
    firstname = fields.StringField(max_length=255)
