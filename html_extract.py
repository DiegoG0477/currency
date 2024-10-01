from bs4 import BeautifulSoup

def extract_text_from_html(html_path):
    """
    Extracts text content from an HTML file.
    """
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    alltext = soup.get_text(separator=' ', strip=True)
    return alltext