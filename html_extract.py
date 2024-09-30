# import selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import pyperclip
# import time

# driver = webdriver.Chrome()
# driver.get("https://www.lazada.com.ph/products/nike-womens-revolution-5-running-shoes-black-i1262506154-s4552606107.html?spm=a2o4l.seller.list.3.6f5d7b6cHO8G2Y&mp=1&freeshipping=1")

# # Scroll down to end of the page to let all javascript code load its content
# lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# match=False
# while(match==False):
#         lastCount = lenOfPage
#         time.sleep(1)
#         lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#         if lastCount==lenOfPage:
#             match=True

# # copy from the webpage
# element = driver.find_element_by_tag_name('body')
# element.send_keys(Keys.CONTROL,'a')
# element.send_keys(Keys.CONTROL,'c')
# alltext = pyperclip.paste()
# alltext = alltext.replace("\n", " ").replace("\r", " ")  # cleaning the copied text
# print(alltext )

from bs4 import BeautifulSoup

# Lee el archivo HTML
with open('html/sevilla.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Analiza el contenido HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extrae el texto del cuerpo del HTML
alltext = soup.get_text(separator=' ', strip=True)

# print(alltext)

def extract_text_from_html(html_path):
    """
    Extracts text content from an HTML file.
    """
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    alltext = soup.get_text(separator=' ', strip=True)
    return alltext