import pandas as pd
from bokeh.charts import Bar, output_file, show


def break_names(df):

    filenames = df['file'].tolist()
    para_nums = []
    titles = []
    for filename in filenames:
        num_and_name = filename.split('/').pop()
        chunks = num_and_name.split('-')
        para_nums.append(chunks[2])
        titles.append(chunks[3])
    df['para_nums'] = pd.Series(para_nums)
    df['titles'] = pd.Series(titles)
    return df


def main():
    data = pd.read_csv('barth_composition_para_only.csv')

    cleaned_data = break_names(data)
    cleaned_data.to_csv('barth_comp_clean.csv')

    columns = cleaned_data.columns.values
    topics = [topic for topic in columns if 'topic' in topic]
    print(topics)

    for topic in topics:
        plot = Bar(
            cleaned_data,
            'para_nums',
            values=topic,
            title="frequency per text of " + topic
        )

        output_file(topic + '.html')
        show(plot)


if __name__ == '__main__':
    main()
