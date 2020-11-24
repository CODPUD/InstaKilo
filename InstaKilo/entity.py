class Account():
    def __init__(self, username):
        self.username = username
        self.id = None
        self.full_name = None
        self.count_follows = None
        self.count_followers = None
        self.count_posts = None

    def update_data(self, data):
        raise NotImplementedError