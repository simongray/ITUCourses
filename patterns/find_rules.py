from patterns.apriori import Apriori
import json
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)


with open('../scraping/dataset/dataset.json', 'r') as dataset_file:
    dataset = json.load(dataset_file)

for key, value in dataset[300].items():
    print(key, '-->', value)


def room_label(room):
    """
    Reduce room string to a label/class.
    """
    if room is None:
        return 'unknown'  # assume 'unknown' if not specified
    room = room.lower()

    # in order of precedence (i.e. 'aud' trumps all)
    if 'aud' in room:
        return 'aud'
    elif 'lab' in room:
        return 'lab'
    elif any(code in room for code in ['1a', '2a', '3a', '4a', '5a']):
        return 'classroom'
    else:
        return 'unknown'   # assume classroom if unknown

overall_high = np.percentile([item['overall_evaluation'] for item in dataset], 75)
overall_low = np.percentile([item['overall_evaluation'] for item in dataset], 25)
overall_median = np.median([item['overall_evaluation'] for item in dataset])
job_high = np.percentile([item['job_evaluation'] for item in dataset], 75)
job_low = np.percentile([item['job_evaluation'] for item in dataset], 25)
job_median = np.median([item['job_evaluation'] for item in dataset])
time_high = np.percentile([item['time_evaluation'] for item in dataset], 75)
time_low = np.percentile([item['time_evaluation'] for item in dataset], 25)
time_median = np.median([item['time_evaluation'] for item in dataset])

participants_median = np.median([item['expected_participants'] for item in dataset])
max_participants_median = np.median([item['maximum_participants'] for item in dataset])

def evaluation_label(evaluation, low, high, high_is_good=True):
    """
    Reduce evaluation to a label.
    """
    if high_is_good:
        if evaluation < low:
            return 'bad'
        elif evaluation >= high:
            return 'good'
        else:
            return 'meh'
    else:
        if evaluation < low:
            return 'good'
        elif evaluation >= high:
            return 'bad'
        else:
            return 'meh'


def timeslot_label(timeslot):
    """
    Reduce timeslots to one of three labels (early, mid, late).
    """
    starting_hour = int(timeslot[:2])

    if starting_hour < 10:
        return 'time:early'
    elif starting_hour >= 16:
        return 'time:late'
    else:
        return 'time:mid'

# prepare room, lecture type, timeslot and lecturer labels
for n, item in enumerate(dataset):
    rooms = []
    times = []

    # merge room info
    for timeslot in item['time_slots']:
        room = timeslot['room']
        lecture = timeslot['type']
        rooms.append(room_label(room)+':'+lecture)
        times.append(timeslot_label(timeslot['time_slot']))  # TODO: concatenate with lecture type too? e.g. "Øvelser:late"

    dataset[n]['rooms'] = set(rooms)
    dataset[n]['times'] = set(times)

    # prepend lecturers with lecturer label
    dataset[n]['lecturers'] = ['lecturer:'+name for name in item['lecturers']]

# find patterns
itemsets = [
    {
        'overall:' + evaluation_label(row['overall_evaluation'], overall_median, overall_median),
        # 'time_evaluation:' + evaluation_label(row['time_evaluation'], time_median, time_median, high_is_good=False),
        # 'job_evaluation:' + evaluation_label(row['job_evaluation'], job_median, job_median),
        'semester:' + row['semester'][0:-5],
        'language:' + row['language'],
        'programme:' + row['programme'],
        'ects:' + str(row['ects_points']),
        'participants:' + ('low' if row['expected_participants'] < participants_median else 'high')#,
        # 'max:' + ('low' if row['maximum_participants'] < max_participants_median else 'high')

    }.union(row['rooms']).union(row['lecturers']).union(row['times'])
    for row in dataset
]

apriori = Apriori(itemsets, 0.01, 0.60, closed_patterns=True)
print("dataset size = " + str(len(apriori.dataset)))

print("\nfrequent patterns, min_support_count = " + str(apriori.min_support_count))
# for itemset in apriori.frequent_patterns:
#     print("{" + ", ".join(sorted(str(item) for item in itemset)) + "}")
#
# print("\nassociation rules, min_confidence = " + str(apriori.min_confidence))
# for a, b in apriori.interesting_rules:
#     print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")
#     print("     lift --> "+str(apriori.lift((a,b))))


# print("\nquality courses")
# for a, b in apriori.association_rules:
#     if 'overall:good' in b and len(b) == 1:
#         print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")
#         print("     lift --> "+str(apriori.lift((a,b))))
#
# print("\nshit courses")
# for a, b in apriori.association_rules:
#     if 'overall:bad' in b and len(b) == 1:
#         print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")
#         print("     lift --> "+str(apriori.lift((a,b))))
# #

with open('good_rules.json', 'w') as rules_file:
    for a, b in apriori.interesting_rules:
        if 'overall:good' in b and len(b) == 1 and len(a) <= 2:
            rules_file.write("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}\n")

with open('bad_rules.json', 'w') as rules_file:
    for a, b in apriori.interesting_rules:
        if 'overall:bad' in b and len(b) == 1 and len(a) <= 2:
            rules_file.write("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}\n")

# with open('rules.json', 'w') as rules_file:
#     for a, b in apriori.interesting_rules:
#         rules_file.write("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}\n")
