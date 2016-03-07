from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks


class AuthenticSession(ApplicationSession):

    # @inlineCallbacks
    def onJoin(self, details):

        def authenticate(realm, authid, details):
             ticket = details['ticket']
             print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', ticket='{}'".format(realm, authid, ticket))

             # Fake auth for the moment, ticket is role !
             return ticket

             # if authid in PRINCIPALS_DB:
             #    if ticket == PRINCIPALS_DB[authid]['ticket']:
             #       return PRINCIPALS_DB[authid]['role']
             #    else:
             #       raise ApplicationError("com.example.invalid_ticket", "could not authenticate session - invalid ticket '{}' for principal {}".format(ticket, authid))
             # else:
             #    raise ApplicationError("com.example.no_such_user", "could not authenticate session - no such principal {}".format(authid))

        return self.register(authenticate, 'xin.authentic.authenticate')
        print("WAMP-Ticket dynamic authenticator registered!")
