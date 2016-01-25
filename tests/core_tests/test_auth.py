import pytest

from scille_core_back.core_app import CoreApp
from scille_core_back.auth import (encrypt_password, verify_password, generate_access_token,
                                   encode_token, decode_token, check_password_strength,
                                   generate_password)

from core_tests.common import BaseTest


class TestCoreAuth(BaseTest):

    @classmethod
    def setup_class(cls):
        return super().setup_class(config={
            'SECRET_KEY': 'test',
            'TOKEN_VALIDITY': 10000,
            'TOKEN_FRESHNESS_VALIDITY': 10000
        })

    def test_password_encrypt_and_decrypt_sucess(self):
        password = "test"
        hash_password = encrypt_password(password)
        assert len(hash_password) != 0
        assert True == verify_password(password, hash_password)

    def test_password_encrypt_and_decrypt_fail(self):
        password = "test"
        hash_password = encrypt_password(password)
        throw = False
        try:
            assert False == verify_password(password, "wrongHash")
        except ValueError:
            throw = True
        assert True == throw
        assert False == verify_password("wrongpassword", hash_password)

    def test_token_encode_and_decode_sucess(self):
        token = generate_access_token("john.doe@nowhere.com",
                                      "password",
                                      fresh=True)
        assert len(token) != 0
        token = decode_token(token)
        assert "john.doe@nowhere.com" == token['email']

    def test_token_decode_fail_due_to_token_freshness(self):
        self.app.config['TOKEN_VALIDITY'] = 100
        token = generate_access_token("john.doe@nowhere.com",
                                      "password",
                                      fresh=True)
        assert len(token) != 0
        token = decode_token(token)
        assert None == token

    def test_check_password_strength(self):
        password_good = "ahahAhah012&"
        password_with_specials = "1Aa!@#$%^&*+-/[]{}\\|=/?><,.;:\'"
        password_to_short = "Short1"
        password_without_majuscule = "nomajuscule12&"
        password_without_minuscule = "01234567aa&"
        password_without_number = "NoNumberInPassword&"
        password_special_not_handle = "éFrenchNotHandle1"

        assert True == check_password_strength(password_good)
        assert True == check_password_strength(password_with_specials)
        assert False == check_password_strength(password_to_short)
        assert False == check_password_strength(password_without_majuscule)
        assert False == check_password_strength(password_without_minuscule)
        assert False == check_password_strength(password_without_number)
        assert False == check_password_strength(password_special_not_handle)

    def test_generate_password(self):
        assert True == check_password_strength(generate_password())
