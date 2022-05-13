#
# https://api.nasa.gov/
#

from math import sqrt
import time
import base64
import requests, json
import markdown as md
import io

########################################################################################################################
class HTMLDoc:

	def __init__(self):
		self.markdown = ''
		self.html = None

	def add_text(self, text):
		self.markdown += text
		self.markdown += '\n'

	def add_bytestring_image(self, bytestring, alt_text = 'alt_text'):
		image_string = '![' + alt_text + '](data:image/png;base64,' + bytestring + ')'
		self.markdown += image_string
		self.markdown += '\n'

	def add_image(self, image, alt_text = 'alt_text'):
		image_string = '![' + alt_text + '](' + image + ')'
		self.markdown += image_string
		self.markdown += '\n'

	def add_css(self, css_file):
		css_string = '<html>\n<head>\n<link rel=\"stylesheet\" href=\"' + css_file + '\">\n</head>'
		self.html = css_string + self.html
		self.html += '</html>'

	def to_html(self):
		self.html = md.markdown(self.markdown)

########################################################################################################################
def _get_image():

    complete_url = 'https://api.nasa.gov/planetary/apod?api_key=82hVmJIh2CbJrwJoltzhCduMVnzCDpIyhFWmqcIY'
    response = requests.get(complete_url)
    x = response.json()

    return x

########################################################################################################################
def _listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele + " "

    # return string
    return str1

########################################################################################################################
def _prepare_html_output(image, copyright, explanation, title):

    text = title

    text += '''

    '''

    explanation = list(explanation.split(" "))
    for i in range(0, len(explanation)):
        if (i%10) == 0:
            explanation.insert(i, "\n")
    explanation = _listToString(explanation)

    text +=  explanation

    text += '''

    '''

    text += 'copyright ' + copyright

    style = '''<html><head>
            <style>
                * {
                font-family: 'Roboto', sans-serif;
                }
                h1 {
                text-align: center;
                }
                p {
                text-align: left;
                }
            </style>
            </head>
            '''

    doc = HTMLDoc()
    doc.add_text(text)
    doc.add_bytestring_image(image)
    doc.to_html()
    doc.html = style + doc.html
    doc.html += '</html'

    return doc.html

########################################################################################################################
def compute():

    image = _get_image()

    response = requests.get(image['url'])
    image_bytes = io.BytesIO(response.content)
    image_bytes = base64.b64encode(image_bytes.getvalue()).decode("utf-8").replace("\n", "")

    output = _prepare_html_output(image_bytes, "", image['explanation'], image['title'])

    return [{'type': 'html', 'label': 'Today', 'data': output}]


########################################################################################################################
def _schema():
    return []
