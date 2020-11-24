class InstagramExceptions(Exception):
    pass

class ConnectionException(InstagramExceptions):
    pass

class AuthException(InstagramExceptions):
    def __init__(self, username):
        super().__init__(f"Can`t auth {username}")