import sys
from ebooklib import epub
import PyPDF2
import os

def pdf_to_epub(pdf_path, epub_path):
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title(os.path.basename(pdf_path))
    book.set_language('en')
    book.add_author('Unknown')

    chapters = []
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text() or ''
        chapter = epub.EpubHtml(title=f'Page {i+1}', file_name=f'page_{i+1}.xhtml', lang='en')
        chapter.content = f'<h1>Page {i+1}</h1><p>{text.replace('\n', '<br/>')}</p>'
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = chapters
    book.spine = ['nav'] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(epub_path, book)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python pdf_to_epub.py input.pdf output.epub')
        sys.exit(1)
    pdf_to_epub(sys.argv[1], sys.argv[2])
    print(f'Converted {sys.argv[1]} to {sys.argv[2]}')
