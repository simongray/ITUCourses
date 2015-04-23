import io
from lxml import html
import requests
import json


def process_course(link_to_course):
    course = requests.get(link_to_course)
    site = html.fromstring(course.text)
    site_data = [
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[2]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[3]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[4]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[5]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[6]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[8]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[9]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[10]//td[2]/text()')
    ]

    time_slots = []
    for i in range(2, 10):
        time_slots.append(
            [
                get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[1]/text()')),
                get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[2]/text()')),
                get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[3]/text()')),
                get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[5]/text()'))
            ])

    site_data = [get_text_from_table_element(element) for element in site_data]
    first_pass = [text.replace(",", "") for text in site_data]
    second_pass = [text.strip() for text in first_pass]

    to_return = {
        'name': second_pass[0],
        'semester': second_pass[1],
        'line_of_studies': second_pass[2],
        'ects': second_pass[3],
        'language': second_pass[4],
        'minimum_participants': second_pass[5],
        'expected_participants': second_pass[6],
        'maximum_participants': second_pass[7],
        'time_slots': convert_to_time_slot_dict(time_slots)
    }

    return to_return


def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def convert_to_time_slot_dict(to_convert):
    converted = []

    for data in to_convert:
        if get_first(data) is None:
            pass
        else:
            as_dict = {
                'day': data[0],
                'time_slot': data[1],
                'type': data[2],
                'room': data[3]
            }
            converted.append(as_dict)

    return converted


def get_text_from_table_element(arr):
    if len(arr) > 0:
        return arr[0]

    return ""


def get_course_links(semester_id):
    page = requests.get('https://mit.itu.dk/ucs/cb_www/index.sml?semester_id=' + semester_id + '&lang=en')
    markup = html.fromstring(page.text)

    links = markup.xpath('//*[@id="course"]//a//@href')
    return links


def scrape_courses(course_list):
    print("Parsing " + str(len(list(course_list))) + " courses...")
    data = []

    for link in course_list:
        processed = process_course(link)
        data.append(processed)

    return data


def save_as_json(to_save, name):
    with io.open(name, 'w', encoding='utf8') as f:
        f.write(to_save)


if __name__ == '__main__':
    semester_ids = ["1475078", "1376480", "1315139", "1226768", "1183866", "1062206", "991552", "912846", "859988",
                    "785862", "717578", "478897", "454681", "409901", "293157", "253799", "235230", "177371"]

    results = []
    for semester in semester_ids:
        courses = ["https://mit.itu.dk" + str(link) for link in get_course_links(semester)]
        scraped = scrape_courses(courses)

        save_as_json(
            json.dumps(scraped, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False),
            "semester_" + semester + ".json")