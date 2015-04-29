import glob
import csv
import json

with_six_questions = [
    '2009october.csv',
    '2010march.csv',
    '2010october.csv',
    '2011march.csv',
    '2011october.csv',
    '2012march.csv',
    '2012october.csv',
    '2013march.csv',
    '2013october.csv',
    '2014march.csv'
]

evaluations = []

for filename in glob.glob("*.csv"):
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')

        for row in reader:
            cleaned_row = {}

            cleaned_row['semester'] = ('Forår ' if 'march' in filename else 'Efterår ') + filename[0:4]
            cleaned_row['programme'] = row['Programme']
            cleaned_row['name'] = row['Course']
            cleaned_row['overall'] = row['q1 average']

            # get percentage of replies
            if row['q1 replies'] != '-':
                replies = row['q1 replies'].split(' ')
                cleaned_row['replies'] = float(replies[0])/float(replies[2])
            else:
                continue

            # for 11 questions, "jobprofil" is q3 and "tidsforbrug" is q10
            # for 6 questions it is q4 and q5, respectively
            if filename in with_six_questions:
                cleaned_row['job'] = row['q4 average']
                cleaned_row['time'] = row['q5 average']
            else:
                cleaned_row['job'] = row['q3 average']
                cleaned_row['time'] = row['q10 average']


            # only keep rows with all the values we need intact
            if all(character not in cleaned_row.values() for character in ['-', '?']):
                # make sure stuff is converted to floats
                for key in cleaned_row.keys():
                    if key in ['job', 'time', 'overall']:
                        cleaned_row[key] = float(cleaned_row[key])

                evaluations.append(cleaned_row)

# save to file
json_string = json.dumps(evaluations, ensure_ascii=False)
with open('all_evaluations.json', 'w') as json_file:
    json_file.write(json_string)
