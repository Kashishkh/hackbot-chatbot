import requests
from bs4 import BeautifulSoup

with open("sample.html", "r"):
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')