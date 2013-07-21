import string

class PageParser:

    def __init__(self):
        self.events = []

    def formURL(self, link, domain):
        # TODO: this is insanely flimsy
        if string.find(link, domain) == -1:
            return domain + link
        return link
