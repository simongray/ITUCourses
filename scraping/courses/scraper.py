import io
from lxml import html
import requests
import json


def __scrape_site(ids):
    for semester in ids:
        course_links = scrape_course_links(semester)
        links = ["https://mit.itu.dk" + str(link) for link in course_links]  # Append base URL to links
        result = scrape_courses(links)

        save_as_json(json.dumps(result,
                                sort_keys=True,
                                indent=4,
                                separators=(',', ': '),
                                ensure_ascii=False),
                     "semester" + semester + ".json")  # Save as json with the correct encoding.


def scrape_course_links(semester_id):
    page = requests.get('https://mit.itu.dk/ucs/cb_www/index.sml?semester_id=' + semester_id + '&lang=en')
    markup = html.fromstring(page.text)

    links = markup.xpath('//*[@id="course"]//a//@href')  # Get every <a href> with the "course" css identifier.
    return links


def scrape_courses(course_list):
    print("Parsing " + str(len(list(course_list))) + " courses...")
    data = []

    for link in course_list:
        processed = __process_course(link)
        data.append(processed)

    return data


def __process_course(link_to_course):
    course = requests.get(link_to_course)
    site = html.fromstring(course.text)

    site_data = __scrape_course_data(site)
    time_slots = __scrape_time_slots(site)
    cleaned = __clean_data(site_data)

    scraped_course = {
        'name': cleaned[0],
        'semester': cleaned[1],
        'line_of_studies': cleaned[2],
        'ects_points': cleaned[3],
        'language': cleaned[4],
        'minimum_participants': cleaned[5],
        'expected_participants': cleaned[6],
        'maximum_participants': cleaned[7],
        'time_slots': __convert_to_time_slot_dict(time_slots)
    }

    return scraped_course


def __scrape_course_data(site):
    # Extract the data needed from the page using the xpath for the html elements containing the data.
    return [
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[2]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[3]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[4]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[5]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[6]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[8]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[9]//td[2]/text()'),
        site.xpath('/html/body/table[2]/tr/td[2]/table[1]/tr[2]/td/form/table//tr[10]//td[2]/text()')
    ]


def __scrape_time_slots(site):
    time_slots = []
    # No course has more than 8 table rows with time slots, therefore extract time slots for eight table rows.
    # If the list returned is empty, there are no time slots. The __get_first function will pass the given empty
    # row.
    for i in range(2, 10):
        time_slots.append(
            [
                __get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[1]/text()')),
                __get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[2]/text()')),
                __get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[3]/text()')),
                __get_first(site.xpath(
                    '/html/body/table[2]/tr/td[2]/table[3]/tr[2]/td/table[1]/tr[' + str(i) + ']/td[5]/text()'))
            ])

    return time_slots


def __clean_data(to_clean):
    # Remove unwanted characters.
    data = [__get_text_from_table(element) for element in to_clean]
    first_pass = [text.replace(",", "") for text in data]
    second_pass = [text.strip() for text in first_pass]
    return second_pass


def __convert_to_time_slot_dict(to_convert):
    converted = []

    for data in to_convert:
        if __get_first(data) is None:
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


def __get_first(iterable, default=None):
    # Get the first element from a list, or None if no element exists.
    if iterable:
        for item in iterable:
            return item
    return default


def __get_text_from_table(arr, default=""):
    # Get the first element from a list, or an empty string if no element exists.
    if arr:
        for item in arr:
            return item
    return default


def save_as_json(to_save, name):
    with io.open(name, 'w', encoding='utf8') as f:
        f.write(to_save)


if __name__ == '__main__':
    semester_ids = ["1475078", "1376480", "1315139", "1226768",
                    "1183866", "1062206", "991552", "912846",
                    "859988", "785862", "717578", "478897",
                    "454681", "409901", "293157", "253799",
                    "235230", "177371"]

    __scrape_site(semester_ids)
