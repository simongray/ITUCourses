from patterns.apriori import Apriori
import json

with open('../scraping/dataset/dataset.json', 'r') as dataset_file:
    dataset = json.load(dataset_file)

for key, value in dataset[300].items():
    print(key, '-->', value)


def room_label(room):
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


# merge room info
for n, item in enumerate(dataset):
    rooms = []

    for timeslot in item['time_slots']:
        room = timeslot['room']
        lecture = timeslot['type']
        rooms.append(room_label(room)+':'+lecture)

    dataset[n]['rooms'] = set(rooms)

print(dataset)


# find patterns
itemsets = [
    {
        'overall_evaluation:' + str(int(row['overall_evaluation'])),
        'semester:' + row['semester'][0:-5]
    }.union(row['rooms'])
    for row in dataset
]

print(itemsets)

apriori = Apriori(itemsets, 0.05, 0.9)
print("dataset size = " + str(len(apriori.dataset)))


print("\nfrequent patterns, min_support_count = " + str(apriori.min_support_count))
for itemset in apriori.frequent_patterns:
    print("{" + ", ".join(sorted(str(item) for item in itemset)) + "}")

print("\nassociation rules, min_confidence = " + str(apriori.min_confidence))
for a, b in apriori.association_rules:
    print("{" + ", ".join(sorted(str(item) for item in a)) + "} => {" + ", ".join(sorted(str(item) for item in b)) + "}")
