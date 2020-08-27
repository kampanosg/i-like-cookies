
class CookieBannerOptions:
    def __init__(self, has_accept_btn=0, cta_accept=None, has_decline_btn=0, cta_decline=None, has_options_btn=0, cta_options=None, has_info_btn=0, cta_info=None, privacy_text=None, website=None):
        self.has_accept_btn = has_accept_btn
        self.cta_accept = cta_accept
        self.has_decline_btn = has_decline_btn
        self.cta_decline = cta_decline
        self.has_options_btn = has_options_btn
        self.cta_options = cta_options
        self.has_info_btn = has_info_btn
        self.cta_info = cta_info
        self.privacy_text = privacy_text
        self.website = website

    @classmethod
    def fromDatabaseRow(cls, row):
        has_accept_btn = row[1]
        cta_accept = row[2]
        has_decline_btn = row[3]
        cta_decline = row[4]
        has_options_btn = row[5]
        cta_options = row[6]
        has_info_btn = row[7]
        cta_info = row[8]
        privacy_text = row[9]
        website = row[10]
        return cls(has_accept_btn, cta_accept, has_decline_btn, cta_decline, has_options_btn, cta_options, has_info_btn, cta_info, privacy_text, website)

    def as_tuple(self):
        return self.website, self.privacy_text, \
            self.has_accept_btn, self.cta_accept, self.has_decline_btn, self.cta_decline, \
            self.has_options_btn, self.cta_options, self.has_info_btn, self.cta_info
