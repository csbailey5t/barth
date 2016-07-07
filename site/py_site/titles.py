import pandas as pd


def main():
    data = pd.read_csv('para_titles.csv')

    titles = data['title']
    titles = titles.tolist()
    cleaned = []
    for title in titles:
        # remove .csv
        pieces = title.split('.')
        # replace '_' with ' '
        words = pieces[0].replace('_', ' ')
        cleaned.append(words)
    data['titles'] = pd.Series(cleaned)
    data.to_csv('titles.csv')


if __name__ == '__main__':
    main()
