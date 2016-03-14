from autobahn.twisted.wamp import ApplicationSession
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.internet.defer import inlineCallbacks, returnValue
from datetime import datetime

from .config import LISTEN_PORT
from .rest import rest_api_factory
from .tools import decode_token


class AuthenticSession(ApplicationSession):

    def onJoin(self, details):

        rest_app = rest_api_factory(self)
        reactor.listenTCP(LISTEN_PORT, Site(rest_app.resource()))

        @inlineCallbacks
        def authenticate(realm, login, details):
            token = decode_token(details['ticket'])
            if not token or login != token['login'] or token['exp'] > datetime.utcnow():
                raise Exception('Invalid token')
            user = yield self.call(RETRIEVE_USER_RPC, login)
            if not user:
                raise Exception('Unknown user')
            print("[AUTHENTIC] WAMP-Ticket dynamic authenticator invoked: realm='{}', "
                  "authid='{}', ticket='{}'".format(realm, login, details))
            returnValue(user.get('role'))

        return self.register(authenticate, 'xin.authentic.authenticate')
        print("WAMP-Ticket dynamic authenticator registered!")


if __name__ == "__main__":
    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)

    wampapp = Application()
    wampapp.run("ws://localhost:8080", "realm1", standalone=False)
