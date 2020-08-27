
class CookieBanner:

    def __init__(self, html='', width=0, height=0, position_x=0, position_y=0, banner_exists=0, website='', banner_hash='', selector='', visit_id=-1):
        self.html = html
        self.width = width
        self.height = height
        self.position_x = position_x
        self.position_y = position_y
        self.banner_exists = banner_exists
        self.website = website
        self.banner_hash = banner_hash
        self.selector = selector
        self.visit_id = visit_id

    def as_tuple(self):
        return self.html, self.width, self.height, self.position_x, self.position_y, \
               self.banner_exists, self.website, self.banner_hash, self.selector, self.visit_id

