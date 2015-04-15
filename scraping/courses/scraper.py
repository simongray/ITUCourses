from lxml import html
import requests
import json

def append_itu(string):
    return "https://mit.itu.dk" + string


def clean_string(string):
    without_newlines = string.rstrip('\n')
    without_tabs = without_newlines.rstrip('\t')
    return without_tabs.rstrip('\r')


def process_link(link):
    course = requests.get(link)
    tree = html.fromstring(course.text)
    text = tree.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr//td[2]/text()')
    return text


def get_course_links(semester_id):
    page = requests.get('https://mit.itu.dk/ucs/cb_www/index.sml?semester_id=' + semester_id + '&lang=en')
    doc_tree = html.fromstring(page.text)
    links = doc_tree.xpath('//*[@id="course"]//a//@href')
    return map(append_itu, links)


def scrape_courses(courses):
    print("Parsing " + str(len(list(courses))) + " courses...")
    print("--------")
    data = []

    for link in courses:
        data.append(process_link(link))

    return data

def find_semester_ids():
    myitu = requests.get('https://mit.itu.dk/ucs/cb_www/index.sml?lang=en')
    tree = html.fromstring(myitu.text)
    semesters = tree.xpath(
        '//tr//td//table//tr[2]//td//table//tr[1]//td[2]//select//option//@value')
    return semesters

# TODO: Make methods async to speed up scraping: http://stevedower.id.au/blog/async-api-for-python/
# TODO: More cleaning of scraped data.
if __name__ == '__main__':
    semesters = find_semester_ids()

    results = []
    count = 1
    for semester in semesters:
        print("")
        print("--------")
        print("Semester " + str(count) + " of " + str(len(semesters)) + ". Id: " + semester)
        courses = get_course_links(semester)
        parsed = scrape_courses(courses)
        results.append(parsed)
        count += 1

    as_json = json.dumps(results)

    with open('results.json', 'w') as f:
    	f.write(as_json)