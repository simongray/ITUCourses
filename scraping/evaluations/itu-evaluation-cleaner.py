import glob
import csv

# for 11 questions, "jobprofil" is q3 and "tidsforbrug" is q10
# for 6 questions it is q4 and q5, respectively

six_questions = [
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
            new_row = {}

            new_row['filename'] = filename
            new_row['programme'] = row['Programme']
            new_row['overall'] = row['q1 average']

            # get percentage of replies
            if row['q1 replies'] != '-':
                replies = row['q1 replies'].split(' ')
                new_row['replies'] = float(replies[0])/float(replies[2])
            else:
                continue

            # for 11 questions, "jobprofil" is q3 and "tidsforbrug" is q10
            # for 6 questions it is q4 and q5, respectively
            if filename in six_questions:
                new_row['job'] = row['q4 average']
                new_row['time'] = row['q5 average']
            else:
                new_row['job'] = row['q3 average']
                new_row['time'] = row['q10 average']


            # only keep rows with all the values we need intact
            if all(character not in new_row.values() for character in ['-', '?']):

                # make sure stuff is converted to floats
                for key in new_row.keys():
                    if key in ['job', 'time', 'overall']:
                        new_row[key] = float(new_row[key])

                evaluations.append(new_row)

print(evaluations)
