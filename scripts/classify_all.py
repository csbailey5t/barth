#!/usr/bin/env python3


import os
import shutil
import traceback

import classify


DEBUG = True
DATADIR = 'data/input/'
OUTPUT = 'output/'
NGRAMS = [
    ('unigram', None),
    ('bigram', '1-2'),
    ('trigram', '1-3'),
]


def run(name, seg_name, seg_range, input_dir, results_csv, select=False,
        output_base=OUTPUT):
    output_dir = os.path.join(
        output_base,
        '{}-{}-{}'.format(name, seg_name, 'select' if select else 'all')
    )

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, True)
    os.makedirs(output_dir)

    args = [
        '--corpus=' + os.path.join(input_dir, 'corpus.csv'),
        '--results=' + results_csv,
        '--feature-file=' + os.path.join(output_dir, 'features.log'),
        '--result-field=chunking:' + name,
        '--result-field=ngrams:' + seg_name,
        '--result-field=selected:' + str(select),
    ]
    if seg_range is not None:
        args.append('--ngram-range=' + seg_range)
    if select:
        args.append('--select-features=0.0')

    try:
        classify.main(args)
    except Exception as ex:
        print('ERROR: {}-{} in {}'.format(name, seg_name, input_dir))
        if DEBUG:
            raise
        else:
            traceback.print_exc()


def main():
    results_file = os.path.join(OUTPUT, 'results.csv')
    print('writing results to "{}"'.format(results_file))
    if os.path.exists(results_file):
        os.remove(results_file)

    for name in os.listdir(DATADIR):
        print(name)
        print('=' * len(name))
        dirname = os.path.join(DATADIR, name)

        for (seg_name, seg_range) in NGRAMS:
            print(seg_name)
            print('-' * len(seg_name))

            run(name, seg_name, seg_range, dirname, results_file, False, OUTPUT)
            run(name, seg_name, seg_range, dirname, results_file, True , OUTPUT)

            print()


if __name__ == '__main__':
    main()
