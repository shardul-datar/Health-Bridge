from flask import Flask, render_template,redirect, url_for, request
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
def altBrandFinder(s):
    url = 'https://www.netmeds.com/prescriptions/'
    s_new = s.lower().replace(' ', '-')
    s_new = re.sub("[%$./()+']", "-", s_new)
    s_new = s_new.replace('-----', '-')
    s_new = s_new.replace('----', '-')
    s_new = s_new.replace('---', '-')
    s_new = s_new.replace('--', '-')
    url += s_new
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    check = soup.find_all('h2', {'class': 'title'})
    if not check:
        try:
            med_name = soup.find('h1', {'class': 'black-txt'}).text
        except AttributeError:
            med_name = "notmentioned"

        try:
            med_price = soup.find('span', {'class': 'price'}).text
        except AttributeError:
            med_price = "notmentioned"

        try:
            med_gen = soup.find('div', {'class': 'drug-manu'}).a.text
        except AttributeError:
            med_gen = "notmentioned"

        try:
            med_manuf = soup.find('span', {'class': 'drug-manu'}).a.text
        except AttributeError:
            med_manuf = "notmentioned"

        try:
            med_uses = soup.find_all('div', {'class': 'inner-content'}).li.text
        except AttributeError:
            med_uses = "Not mentioned"

    alt_meds = []
    meds = soup.find_all('div', class_="drug_list")
    if len(meds) != 0:
        for med in meds:
            more_info = med.a['href']
            alt_meds.append([med.find('a').text, f'https://www.netmeds.com/{more_info}'])

    return alt_meds

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        s = request.form['content']
        alt_brands = altBrandFinder(s)
        return render_template('alt_brands.html', alt_brands=alt_brands)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)