class UserAccount:
    def __init__(self, username, password, likePercentage, commentPercentage, numInteract, hashtags, default):
        self.username = username
        self.password = password
        self.likePercentage = likePercentage
        self.commentPercentage = commentPercentage
        self.numInteractions = numInteract
        self.commentList = []
        self.hashtags = hashtags
        self.default = default
    
    def setDefault(self):
        self.default = 1