"""@package docstring
The user module provide the simpliest representation of a user:
    -email
    -password
example: {'email': "jhon.doe@nowhere.com", 'password': "encrypted_password"}
"""
from datetime import datetime
from mongoengine import ValidationError
from core.model_util import BaseController, BaseSolrSearcher, BaseDocument, fields
from flask.ext.principal import Identity, UserNeed


class UserDocumentController(BaseController):
    meta = {'allow_inheritance': True}

    """
    The controller of the Simple User Document
    """

    def clean(self):
        """
        Check if the user has at least an email, if not
        throw a ValidationError
        """
        if not self.document.email:
            raise ValidationError(errors={'email':
                                          'This field is mandatory'})

    def set_password(self, password):
        """Store the password encrypted (i.e. hashed&salted)"""
        from core.auth import encrypt_password, check_password_strength
        if check_password_strength(password):
            self.document.password = encrypt_password(password)
            return True
        return False

    def close_user(self, end_validity=None):
        """
        Close the user at the end of validity parameter or at datetime.utcnow
        """
        if not self.document.fin_validite:
            self.document.fin_validite = end_validity or datetime.utcnow()
            return True
        else:
            # user already closed
            return False

    def load_in_app(self, app):
        identity = Identity(str(self.document.id))
        identity.provides.add(UserNeed(self.document.id))
        return identity


class UserDocumentSearcher(BaseSolrSearcher):
    meta = {'allow_inheritance': True}
    """
    Search a user based on its email
    """
    FIELDS = ('email')


class UserDocument(BaseDocument):

    """
    This is the minimal model representation of User, you are free to extend this document
    in your application
    """
    meta = {'controller_cls': UserDocumentController,
            'searcher_cls': UserDocumentSearcher, 'allow_inheritance': True}
    email = fields.EmailField(max_length=255, required=True, unique=True)
    password = fields.StringField(max_length=255)
    # needed for the token validity
    fin_validite = fields.DateTimeField(null=True)
