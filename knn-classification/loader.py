__author__ = 'Anders'

import json
import numpy as numpy
import converter


def __load_courses():
    courses = []
    courses_file = open('dataset.json', 'r')
    courses.extend(json.load(courses_file))
    courses_file.close()
    return courses


def all_evaluation_data():
    courses = __load_courses()
    as_numpy = []
    target_data = []

    for course in courses:
        nd_array = numpy.array([
            course["ects_points"],
            course["expected_participants"],
            course["job_evaluation"],
            converter.convert_language(course["language"]),
            converter.convert_line_of_studies(course["line_of_studies"]),
            course["maximum_participants"],
            course["minimum_participants"],
            course["replies"],
            converter.convert_semester(course["semester"]),
            course["time_evaluation"]
        ])

        as_numpy.append(nd_array)

        # Set target for given course by its overall evaluation in three categories.
        # if below 4.45 => low
        # if over 5.4 => high
        evaluation = course["overall_evaluation"]
        if evaluation <= 4.45:
            target_data.append("bad course rating")
        elif evaluation > 5.4:
            target_data.append("good course rating")
        else:
            target_data.append("medium course rating")

    return numpy.array(as_numpy), numpy.array(target_data)


def training_data():
    x, y = all_evaluation_data()

    return x[:-100]


def test_data():
    x, y = all_evaluation_data()

    return x[-100:]

if __name__ == '__main__':
    lol = test_data()