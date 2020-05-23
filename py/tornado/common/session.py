import os, time
from hashlib import sha1

# Generate session_id randomly
create_session_id = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()

class Session:
    # diy session

    info_container = {
        # session_id: {'user': info} --> Save user information, permissions, etc. via session
    }

    def __init__(self, handler):
        self.handler = handler

        # Get a random string as a session_id from the cookie, or generate a session_id if there is no or no match.
        random_str = self.handler.get_cookie('session_id')
        if (not random_str) or (random_str not in self.info_container):
            random_str = create_session_id()
            self.info_container[random_str] = {}
        self.random_str = random_str

        # Call set_cookie after each request.Ensure that the expiration time of each reset is XX seconds after the current time.
        self.handler.set_cookie('session_id', random_str, max_age=60)

    def __getitem__(self, item):
        return self.info_container[self.random_str].get(item)

    def __setitem__(self, key, value):
        self.info_container[self.random_str][key] = value

    def __delitem__(self, key):
        if self.info_container[self.random_str].get(key):
            del self.info_container[self.random_str][key]

    def delete(self):
        del self.info_container[self.random_str]

class SessionHandler:
    def initialize(self):
        self.session = Session(self)  # handler add session property