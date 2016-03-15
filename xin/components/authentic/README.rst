Authentic user autenticator
===========================

Config vars:

- ``SECRET_KEY``
- ``REGISTER_USER_RPC``
- ``RETRIEVE_USER_RPC``
- ``LISTEN_PORT``
- ``TOKEN_VALIDITY``


RPC to provide:

register_user(login, hashed_password) -> {'login': <>, 'hashed_password': <>, 'role': <>}

retrieve_user(login) -> {'login': <>, 'hashed_password': <>, 'role': <>}
