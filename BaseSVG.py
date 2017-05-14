

class BaseSVG:
    def __init__(self, width, height):
        w = str(width)
        h = str(height)
        self.header = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
    version="1.1"
    width="''' + w + '"' + "\n"
        self.header = self.header + '    height="' + h + '"' + "\n"
        self.header = self.header + '    viewBox="0 0 '
        self.header = self.header + w + ' ' + h + '">' + "\n"
        self.header = self.header + '''<title>TS SVG Art Generator</title>
<desc>SVG Art Creator by Thomas Suchyta</desc>'''

        self.footer = '</svg>'

    def __repr__(self):
        return self.header + "\n" + self.footer
