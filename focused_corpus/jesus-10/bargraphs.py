import pandas as pd
from bokeh.charts import Bar, output_file, show


def break_names(df):
    """Parse filenames into paragraph numbers and titles, adding those
    into the dataframe"""

    filenames = df['file'].tolist()
    chunk_num = []
    for filename in filenames:
        chunks = filename.split('-')
        chunk_num.append(chunks[4])
    df['chunk_num'] = pd.Series(chunk_num)
    return df


def main():
    data = pd.read_csv('paragraph_composition.csv')

    # cleaned_data = break_names(data)
    # Save a copy of the manipulated data for later use
    # cleaned_data.to_csv('barth_composition_clean.csv')

    columns = data.columns.values
    topics = [topic for topic in columns if 'topic' in topic]

    for topic in topics:
        plot = Bar(
            data,
            'id',
            values=topic,
            ylabel='Proportion',
            xlabel='Paragraph Number',
            title="Proportion per pararaph of " + topic
        )

        output_file(topic + '.html')
        show(plot)


if __name__ == '__main__':
    main()
