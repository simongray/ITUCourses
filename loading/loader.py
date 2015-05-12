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


def numerical_evaluation_data(eval_data):
    courses = load_courses()
    as_numpy = []
    target_data = []

    for course in courses:
        if eval_data:
            nd_array = numpy.array([
                course["overall_evaluation"],
                # converter.java_string_hashcode(course["name"]),
                converter.convert_ects(course["ects_points"]),
                course["expected_participants"],
                # course["maximum_participants"],
                course["minimum_participants"],
                converter.convert_time_slots(course["time_slots"]),
                converter.convert_language(course["language"]),
                converter.convert_line_of_studies(course["line_of_studies"]),
                converter.convert_semester(course["semester"]),
            ])

        else:
            nd_array = numpy.array([
                # converter.java_string_hashcode(course["name"]),
                converter.convert_ects(course["ects_points"]),
                course["expected_participants"],
                # course["maximum_participants"],
                course["minimum_participants"],
                converter.convert_time_slots(course["time_slots"]),
                converter.convert_language(course["language"]),
                converter.convert_line_of_studies(course["line_of_studies"]),
                converter.convert_semester(course["semester"]),
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


def normalised_evaluation_data():
    courses, y = numerical_evaluation_data()

    # Participants
    # participants = [courses[i][0] for i in range(0, len(courses))]
    # max_participants = max(participants)
    # min_participants = min(participants)

    # Job evaluation
    job_evaluations = [courses[i][0] for i in range(0, len(courses))]
    max_evaluation = max(job_evaluations)
    min_evaluation = min(job_evaluations)

    # Line of studies
    # lines = [courses[i][4] for i in range(0, len(courses))]
    # max_line = max(lines)
    # min_line = min(lines)

    # Replies
    replies = [courses[i][1] for i in range(0, len(courses))]
    max_replies = max(replies)
    min_replies = min(replies)

    # Time evaluations
    time_evaluations = [courses[i][2] for i in range(0, len(courses))]
    max_time_eval = max(time_evaluations)
    min_time_eval = min(time_evaluations)

    normalised = []
    for course in courses:
        # course[0] = converter.normalise(course[1], max_participants, min_participants)
        course[0] = converter.normalise(course[0], max_evaluation, min_evaluation)
        # course[4] = converter.normalise(course[4], max_line, min_line)
        course[1] = converter.normalise(course[1], max_replies, min_replies)
        course[2] = converter.normalise(course[2], max_time_eval, min_time_eval)
        normalised.append(course)

    return normalised


def get_labels():
    return ["ects_points", "expected_participants", "job_evaluation", "language", "line_of_studies",
            "maximum_participants", "minimum_participants", "replies", "semester", "time_evaluation",
            "overall_evaluation"]


def training_data():
    x, y = numerical_evaluation_data()

    return x[:-100]


def test_data():
    x, y = numerical_evaluation_data()

    return x[-100:]


if __name__ == '__main__':
    numerical_evaluation_data(eval_data=False)