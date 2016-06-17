import pandas as pd

sources = [
    'models/full60/categorized_topics.csv',
    'models/mallet-before/categorized_topics_before.csv',
    'models/mallet-after/categorized_topics_after.csv',
]


def main():
    for source in sources:
        # Need to get list of different doctrines
        # then count instances
        # read in the csv
        topics = pd.read_csv(source)
        # get just the 'Doctrine' column
        doctrines = topics.Doctrine.tolist()
        doctrine_list = []
        for doctrine in doctrines:
            words = doctrine.split(' ')
            for word in words:
                word.strip()
                doctrine_list.append(word)

        print(doctrine_list)


if __name__ == '__main__':
    main()

# names = set()
# for phrase in doctrines:
#     phrase = str(phrase)
#     words = phrase.split(' ')
#     for word in words:
#         names.add(word)
# name_count = []
# for name in names:
#     count = len(doctrines[doctrines == name])
#     name_count.append([name, count])
#     print(doctrines[doctrines == name])
# count_election = doctrines[doctrines == 'Election']
# print(source, name_count)
