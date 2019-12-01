class UserAccount:
    def __init__(self, accountType, email, password, numInteract, hashtags, users, id):
        self.accountType = accountType
        self.email = email
        self.password = password
        self.numInteractions = numInteract
        self.commentList = []
        self.hashtags = hashtags
        self.users = users
        self.id = id
    
    def setDefault(self):
        self.default = 1
        #User Doc Format: accountType, email, password, numInteractions, hashtags, users