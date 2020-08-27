
class DbCookieBanner:
    def __init__(self, row=None):
        self.cookie_id = row[0]
        self.html = row[1]
        self.width = row[2]
        self.height = row[3]
        self.position_x = row[4]
        self.position_y = row[5]
        self.has_cookie_banner = row[6]
        self.website = row[7]
        self.hash = row[8]
        self.selector = row[9]