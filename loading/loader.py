__author__ = 'Anders'

import json

import numpy as numpy

from loading import converter


def load_courses():
    courses = []
    courses_file = open('../scraping/dataset/dataset.json', 'r')
    courses.extend(json.load(courses_file))
    courses_file.close()
    return courses


def all_evaluation_data():
    courses = load_courses()
    as_numpy = []
    target_data = []

    for course in courses:
        nd_array = numpy.array([
            converter.java_string_hashcode(course["name"]),
            course["ects_points"],
            course["expected_participants"],
            course["job_evaluation"],
            converter.convert_language(course["language"]),
            converter.convert_line_of_studies(course["line_of_studies"]),
            course["maximum_participants"],
            course["minimum_participants"],
            course["replies"],
            converter.convert_semester(course["semester"]),
            course["time_evaluation"],
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


def get_labels():
    course = load_courses()

    return ["ects_points", "expected_participants", "job_evaluation", "language", "line_of_studies",
            "maximum_participants", "minimum_participants", "replies", "semester", "time_evaluation",
            "overall_evaluation"]


def training_data():
    x, y = all_evaluation_data()

    return x[:-100]


def test_data():
    x, y = all_evaluation_data()

    return x[-100:]


if __name__ == '__main__':
    lol = test_data()