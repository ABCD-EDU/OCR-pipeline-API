from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextBoxHorizontal

from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator

def getTokensInPage(page):
    layout = page
    x, y, text, face, size = -1, -1, '', "", -1
    tokens = []
    for textbox in layout:
        if isinstance(textbox, LTText):
            for line in textbox:
                for char in line:
                    # If the char is a line-break or an empty space, the word is complete
                    if isinstance(char, LTAnno) or char.get_text() == ' ':
                        if x != -1:
                            obj = {
                                "x":x,
                                "y":y,
                                "text":text,
                                "face":face,
                                "size":size
                            }
                            tokens.append(obj)
                        x, y, text = -1, -1, ''     
                    elif isinstance(char, LTChar):
                        text += char.get_text()
                        if x == -1:
                            x, y, = char.bbox[0], char.bbox[3]
                            face, size = char.fontname, char.size
    return tokens

def constructSentences(tokens):
    sentences = []
    sentence = ""
    for token in tokens:
        text = token["text"]
        # Add it to sentence if it is a period or a bullet point
        if text[-1] == "." or text == "•":
            if text == "•":
                sentences.append(sentence)
                sentence = "•"
            if text[-1] == ".":
                sentence += " " + text
                sentences.append(sentence)
                sentence = ""
        else:
            sentence += " " + token["text"]

    sentences = [x.strip() for x in sentences if x.strip() != ""]
    return sentences

class PDFParser:
    def __init__(self, src):
        self.src = src

    def parsePDF(self):
        pages = {}
        for page_num, page in enumerate(extract_pages(self.src), 1):
            page_data = {}
            returned = getTokensInPage(page)
            sentences = constructSentences(returned)
            page_data["sentences"] = sentences
            page_data["tokens"] = returned
            pages[page_num] = page_data

            return pages
            if page_num == 2:
                return pages

# path = "C:/Users/chris/repos/mining/OCR-pipeline-API/res/sample1.pdf"
# parser = PDFParser(path)
# returned = parser.parsePDF()
# print(returned)