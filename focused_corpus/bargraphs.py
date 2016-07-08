import pandas as pd
from bokeh.charts import Bar, output_file, show


def break_names(df):
    """Parse filenames into paragraph numbers and titles, adding those
    into the dataframe"""

    filenames = df['file'].tolist()
    para_num = []
    for filename in filenames:
        chunks = filename.split('-')
        num_and_ext = chunks[3].split('.')
        num = num_and_ext[0]
        para_num.append(num)
    df['para_num'] = pd.Series(para_num)
    return df


def main():
    data = pd.read_csv('composition.csv')
    cleaned_data = break_names(data)
    # Save a copy of the manipulated data for later use
    # cleaned_data.to_csv('barth_composition_clean.csv')

    columns = cleaned_data.columns.values
    topics = [topic for topic in columns if 'topic' in topic]
    for topic in topics:
        plot = Bar(
            cleaned_data,
            'para_num',
            values=topic,
            ylabel='Proportion',
            xlabel='Paragraph Number',
            title="Proportion per pararaph of " + topic
        )

        output_file('paragraph_figures/' + topic + '.html')
        show(plot)


if __name__ == '__main__':
    main()
