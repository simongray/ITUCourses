import json
import glob

# load evaluations
with open('../evaluations/all_evaluations.json', 'r') as evaluations_file:
    evaluations = json.load(evaluations_file)

# load courses
courses = []
for filename in glob.glob("../courses/*.json"):
    courses_file = open(filename, 'r')
    courses.extend(json.load(courses_file))
    courses_file.close()

# merge into single dataset
dataset = []
for course in courses:
    for evaluation in evaluations:
        if course['name'] == evaluation['name'] and course['semester'] == evaluation['semester']:
            course.update(evaluation)
            dataset.append(course)

# convert strings to numbers where needed
for n, item in enumerate(dataset):
    item['minimum_participants'] = int(item['minimum_participants'])
    item['maximum_participants'] = int(item['maximum_participants'])
    item['expected_participants'] = int(item['expected_participants'])
    item['ects_points'] = int(item['ects_points'])
    dataset[n] = item

with open('dataset.json', 'w') as dataset_file:
    dataset_file.write(json.dumps(dataset, ensure_ascii=False))

print('dataset length:', len(dataset))
