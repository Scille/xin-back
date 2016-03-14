import json
from datetime import datetime
from klein import Klein
from twisted.internet.defer import inlineCallbacks, returnValue

from .tools import encrypt_password, verify_password, encode_token, decode_token
from .config import RETRIEVE_USER_RPC, REGISTER_USER_RPC, TOKEN_VALIDITY


class Response400(Exception):
    pass


def _retreive_content(request):
    try:
        body = json.loads(request.content.read().decode())
    except ValueError:
        raise Response400('Invalid JSON body.')
    login = body.get('login')
    password = body.get('password')
    if type(login) is not str or type(password) is not str:
        raise Response400('Missing or invalid login and/or password.')
    return login, password


def rest_api_factory(wamp_session):

    klein_app = Klein()


    @klein_app.handle_errors(Response400)
    def response_400(request, failure):
        request.setResponseCode(400)
        return json.dumps({'message': str(failure.value)})

    @klein_app.route('/login', methods = ['POST'])
    @inlineCallbacks
    def login(request):
        login, password = _retreive_content(request)
        user = yield wamp_session.call(RETRIEVE_USER_RPC, login)
        if not user or not verify_password(password, user.get('hashed_password')):
            raise Response400('Unknown user or invalid password')
        exp = datetime.utcnow().timestamp() + TOKEN_VALIDITY
        token = encode_token({'login': login, 'exp': exp})
        returnValue(json.dumps({'token': token}))

    @klein_app.route('/signin', methods = ['POST'])
    @inlineCallbacks
    def signin(request):
        login, password = _retreive_content(request)
        hashed_password = encrypt_password(password)
        user = yield wamp_session.call(REGISTER_USER_RPC, login, hashed_password)
        if not user:
            raise Response400("Couldn't create user")
        returnValue(json.dumps({'login': login}))

    # @klein_app.route('/login/github')
    # @inlineCallbacks
    # def login_github(request):
    #   pass

    return klein_app
