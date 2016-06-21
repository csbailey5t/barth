import pandas as pd
from bokeh.charts import Bar, output_file, show


def break_names(df):
    """Parse filenames into paragraph numbers and titles, adding those
    into the dataframe"""

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
    # Save a copy of the manipulated data for later use
    cleaned_data.to_csv('barth_composition_clean.csv')

    columns = cleaned_data.columns.values
    topics = [topic for topic in columns if 'topic' in topic]

    for topic in topics:
        plot = Bar(
            cleaned_data,
            'para_nums',
            values=topic,
            ylabel='Proportion',
            xlabel='Paragraph Number',
            title="Proportion per pararaph of " + topic
        )

        output_file(topic + '.html')
        show(plot)


if __name__ == '__main__':
    main()
