from bs4 import BeautifulSoup
import requests

r = requests.get('https://mit.itu.dk/ucs/evaluation/public.sml?lang=english')
semester_page = r.text
soup = BeautifulSoup(semester_page)

semesters = [period.get('value') for period in soup.find_all('option')]

params = {
    'report': '2',
    'format': 'download',
    'lang': 'english',
    'profile': 'internet'
}

for semester in semesters:
    params['dir'] = semester
    r = requests.post('https://mit.itu.dk/ucs/evaluation/evaluation_fase2_interpret_logon.sml', params=params)

    with open(semester + '.csv', 'w') as csv_file:
        csv_file.write(r.text)
