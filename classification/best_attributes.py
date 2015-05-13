from random import shuffle
from classification.knn import KNearestNeighbors
from shared.utils import mode, powerset, normalize
import json
import numpy as np


with open('../scraping/dataset/dataset.json', 'r') as dataset_file:
    dataset = json.load(dataset_file)

attributes = dataset[0].keys()
dataset = normalize(dataset)


print("\npredicting programme from different attributes")
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
classification_dataset = [
    {
        'overall': evaluation_label(row['overall_evaluation'], overall_median, overall_median),
        # 'time_evaluation': evaluation_label(row['time_evaluation'], time_median, time_median, high_is_good=False),
        # 'job_evaluation': evaluation_label(row['job_evaluation'], job_median, job_median),
        'semester': row['semester'][0:-5],
        'language': row['language'],
        'programme': row['programme'],
        'ects': str(row['ects_points']),
        'participants': ('low' if row['expected_participants'] < participants_median else 'high'),
        'rooms': row['rooms'],
        'lecturers': row['lecturers'],
        'times': row['times']
    }
    for row in dataset
]

print('dataset size =', len(dataset))

# find every possible combination of keys in the dataset
subsets = [
    set(subset)
    for subset in powerset([key for key in classification_dataset[0].keys() if key != 'degree'])
    if subset
]
results = []

for i, subset in enumerate(subsets):
    # create temporary dataset to extract test and training sets from
    temp_dataset = [
        {
            attribute: row[attribute]
            for attribute in subset.union({'overall'})  # every set MUST contain the name/class of the course
        }
        for row in classification_dataset
    ]
    ignored = ['overall']

    for k in [1, 3, 5]:
        print('trying with k =', k)
        cumulative_success_rate = 0

        # test each subset of features 10 times
        for n in range(10):
            # extract the test and training sets
            shuffle(temp_dataset)
            test_set = temp_dataset[:len(dataset)//10]
            training_set = temp_dataset[len(dataset)//10:]

            # make sure we reset before every test
            bad_predictions = 0

            # perform the actual accuracy test
            for datapoint in test_set:
                neighbors = KNearestNeighbors.neighbors(k=k, unknown_datapoint=datapoint, dataset=training_set, ignored=ignored)
                if datapoint['overall'] != mode(neighbors, 'overall'):
                    bad_predictions += 1

            # calculate prediction success
            success_rate = (len(test_set)-bad_predictions)/len(test_set)
            if success_rate > 1:
                raise Exception("something went wrong, success > 1.0")

            cumulative_success_rate += success_rate

        # store result for each combination of k and features
        results.append((cumulative_success_rate, subset, k))

    print('done with ' + str(i+1) + ' out of ' + str(len(subsets)))

results = sorted(results, key=lambda r: r[0], reverse=True)

for n, row in enumerate(results):
    if n < 25:
        print(str(row[0]) + '%', row[1], 'k:', row[2])

with open('classifier_results.txt', 'w') as results_file:
    results_file.writelines([str(result)+"\n" for result in results])
