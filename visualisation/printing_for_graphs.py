from loading import loader

data = loader.load_courses()


def convert_semester(string):
    if "Forår" in string:
        return string[-4:] + "A"
    else:
        return string[-4:] + "B"


for course in data:
    to_print = course["name"] + "	" + convert_semester(course["semester"]) + "	" + str(
        course["overall_evaluation"]) + "	" + str(course["ects_points"]) + "	" + str(course["expected_participants"]) + \
        "	" + str(course["job_evaluation"]) + "	" + course["language"] + "	" + str(course["replies"]) + "	" + \
        str(course["time_evaluation"])

    for lecturer in course["lecturers"]:
        to_print += "	" + lecturer

    print(to_print)

