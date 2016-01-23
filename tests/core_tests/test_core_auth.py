from core.core_app import CoreApp
from core.auth import (encrypt_password, verify_password, generate_access_token,
                       encode_token, decode_token, check_password_strength,
                       generate_password)


class AuthTestApp:

    def __init__(self):
        self.app = CoreApp("TestDecode")
        self.app.bootstrap()
        self.app.config['SECRET_KEY'] = "test"
        self.app.config['TOKEN_VALIDITY'] = 10000
        self.app.config['TOKEN_FRESHNESS_VALIDITY'] = 10000

    def get(self):
        return self.app


def test_password_encrypt_and_decrypt_sucess():
    password = "test"
    hash_password = encrypt_password(password)
    assert len(hash_password) != 0
    assert True == verify_password(password, hash_password)


def test_password_encrypt_and_decrypt_fail():
    password = "test"
    hash_password = encrypt_password(password)
    throw = False
    try:
        assert False == verify_password(password, "wrongHash")
    except ValueError:
        throw = True
    assert True == throw
    assert False == verify_password("wrongpassword", hash_password)


def test_token_encode_and_decode_sucess():
    app = AuthTestApp().get()
    with app.app_context():
        token = generate_access_token("john.doe@nowhere.com",
                                      "password",
                                      fresh=True)
        assert len(token) != 0
        token = decode_token(token)
        assert "john.doe@nowhere.com" == token['email']


def test_token_decode_fail_due_to_token_freshness():
    app = AuthTestApp().get()
    app.config['TOKEN_VALIDITY'] = 100
    with app.app_context():
        token = generate_access_token("john.doe@nowhere.com",
                                      "password",
                                      fresh=True)
        assert len(token) != 0
        token = decode_token(token)
        assert None == token


def test_check_password_strenght():
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


def test_generate_password():
    assert True == check_password_strength(generate_password())
