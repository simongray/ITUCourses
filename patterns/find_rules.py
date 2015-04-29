from patterns.apriori import Apriori
import json
import numpy as np

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


# merge room info
for n, item in enumerate(dataset):
    rooms = []

    for timeslot in item['time_slots']:
        room = timeslot['room']
        lecture = timeslot['type']
        # time = timeslot['time_slot']  # TODO: use this at all?
        # rooms.append(room_label(room)+':'+lecture+':'+time)
        rooms.append(room_label(room)+':'+lecture)

    dataset[n]['rooms'] = set(rooms)

print(dataset)

# find patterns
itemsets = [
    {
        'overall:' + evaluation_label(row['overall_evaluation'], overall_median, overall_median),
        # 'time_evaluation:' + evaluation_label(row['time_evaluation'], time_median, time_median, high_is_good=False),
        # 'job_evaluation:' + evaluation_label(row['job_evaluation'], job_median, job_median),
        'semester:' + row['semester'][0:-5],
        'language:' + row['language'],
        'programme:' + row['programme'],
        #'ects:' + str(row['ects_points']),
        'participants:' + ('low' if row['expected_participants'] < participants_median else 'high'),
        'max:' + ('low' if row['maximum_participants'] < max_participants_median else 'high')

    }.union(row['rooms'])
    for row in dataset
]

print(itemsets)

apriori = Apriori(itemsets, 0.02, 0.75)
print("dataset size = " + str(len(apriori.dataset)))


print("\nfrequent patterns, min_support_count = " + str(apriori.min_support_count))
# for itemset in apriori.frequent_patterns:
#     print("{" + ", ".join(sorted(str(item) for item in itemset)) + "}")

print("\nassociation rules, min_confidence = " + str(apriori.min_confidence))
# for a, b in apriori.association_rules:
#     print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")

print("\nquality courses")
for a, b in apriori.association_rules:
    if 'overall:good' in b and len(b) == 1:
        print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")

print("\nshit courses")
for a, b in apriori.association_rules:
    if 'overall:bad' in b and len(b) == 1:
        print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")

