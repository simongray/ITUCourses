from lxml import html
import requests


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
    tree = html.fromstring(page.text)
    links = tree.xpath('//*[@id="course"]//a//@href')
    return map(append_itu, links)


def scrape_courses(courses):
    link_count = len(courses)
    count = 0
    data = []

    for link in courses:
        data.append(process_link(link))
        count += 1
        print str(count) + " of " + str(link_count)

    return data

#TODO: Get every semester programmatically.
#TODO: Make methods async to speed up scraping.
#TODO: More cleaning of scraped data.
if __name__ == '__main__':
    courses = get_course_links('1662789')
    parsed = scrape_courses(courses)
    print parsed