class UserContext:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        """Returns the username."""
        return self.username

    def get_password(self):
        """Returns the password."""
        return self.password

def get_user_context(username, password):
    """Returns an instance of UserContext with the provided username and password."""
    return UserContext(username, password)
