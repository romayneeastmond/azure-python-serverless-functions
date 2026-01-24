from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO

def generate_pdf_document(content):
    byte_stream = BytesIO()
    doc = SimpleDocTemplate(byte_stream, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    soup = BeautifulSoup(content, 'html.parser')

    def add_element_to_story(element):
        text = element.get_text(strip=True)
        
        if not text and element.name not in ['br', 'hr']:
             return

        if element.name == 'h1':
            story.append(Paragraph(text, styles['Heading1']))
            story.append(Spacer(1, 12))
        elif element.name == 'h2':
            story.append(Paragraph(text, styles['Heading2']))
            story.append(Spacer(1, 10))
        elif element.name == 'h3':
            story.append(Paragraph(text, styles['Heading3']))
            story.append(Spacer(1, 8))
        elif element.name == 'p':
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 12))
        elif element.name == 'ul':
            list_items = []
            for li in element.find_all('li'):
                list_items.append(ListItem(Paragraph(li.get_text(strip=True), styles['Normal'])))
            story.append(ListFlowable(list_items, bulletType='bullet', start='circle'))
            story.append(Spacer(1, 12))
        elif element.name == 'ol':
            list_items = []
            for li in element.find_all('li'):
                list_items.append(ListItem(Paragraph(li.get_text(strip=True), styles['Normal'])))
            story.append(ListFlowable(list_items, bulletType='1'))
            story.append(Spacer(1, 12))
        elif element.name == 'strong' or element.name == 'b':             
             story.append(Paragraph(f"<b>{text}</b>", styles['Normal']))
        elif element.name == 'em' or element.name == 'i':
             story.append(Paragraph(f"<i>{text}</i>", styles['Normal']))
        elif element.name:
             story.append(Paragraph(text, styles['Normal']))
             story.append(Spacer(1, 12))

    for element in soup.contents:
        if element.name:
            add_element_to_story(element)

    try:
        doc.build(story)
        return byte_stream.getvalue()
    except Exception as e:
        return b""

