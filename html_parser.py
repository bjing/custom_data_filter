from HTMLParser import HTMLParser

"""
    Borrowed code from the internet for stripping HTML markups
"""

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
        self.containstags = False

    def handle_starttag(self, tag, attrs):
        self.containstags = True

    def handle_data(self, d):
        self.fed.append(d)

    def has_tags(self):
        return self.containstags

    def get_data(self):
        return ''.join(self.fed)

def strip_html_tags(html):
    must_filtered = True
    while ( must_filtered ):
        s = MLStripper()
        s.feed(html)
        html = s.get_data()
        must_filtered = s.has_tags()
    return html 
