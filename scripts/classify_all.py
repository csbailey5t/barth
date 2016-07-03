#!/usr/bin/env python3


from collections import namedtuple
import csv
import os
from multiprocessing import Pool
import sys

import classify


DEBUG = True
DATADIR = 'data/input/'
OUTPUT = 'output/'
NGRAMS = [
    ('unigram', None),
    ('bigram', '1-2'),
    ('trigram', '1-3'),
]

ArgTuple = namedtuple(
    'ArgTuple',
    ('corpus', 'ratio', 'feature_file', 'ngram_range', 'select_features',
        'result_fields',)
)
Job = namedtuple(
    'Job',
    ('cls', 'args', 'chunking', 'ngrams', 'selected')
)
Result = namedtuple(
    'Result',
    ('chunking', 'ngrams', 'selected') + tuple(classify.RESULTS_HEADER),
)
RESULT_FIELDS = set(Result._fields)


def run_all(input_dir, output_base, ngram_ranges):
    with Pool() as pool:
        jobs = all_jobs(input_dir, output_base, ngram_ranges)
        yield from pool.map(classify_job, jobs)


def classify_job(job):
    all_results = []
    job_str = str(job)
    sys.stdout.write('START: {}\n'.format(job_str))
    sys.stdout.flush()

    try:
        results = classify.classify_job((job.cls, job.args))

        for result in results:
            result.update(
                chunking=job.chunking,
                ngrams=job.ngrams,
                selected=job.selected,
            )
            all_results.append(Result(**{
                k: v for (k, v) in result.items() if k in RESULT_FIELDS
            }))

    except ValueError:
        results = []

    sys.stdout.write('END  : {}\n'.format(job_str))
    sys.stdout.flush()
    return all_results


def all_jobs(input_dir, output_base, ngram_options):
    for name in os.listdir(input_dir):
        dirname = os.path.join(input_dir, name)
        name_args = ArgTuple(
            corpus=os.path.join(dirname, 'corpus.csv'),
            ratio=0.2,
            feature_file=None,
            ngram_range=None,
            select_features=None,
            result_fields={},
        )

        for (seg_name, seg_range) in ngram_options:
            seg_args = name_args._replace(ngram_range=seg_range)

            for select in (None, 0.0, 0.1, 0.2, 0.3):
                output_dir = os.path.join(
                    output_base,
                    '{}-{}-{}'.format(
                        name,
                        seg_name,
                        str(select) if select is not None else 'all',
                    ))
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                args = seg_args._replace(
                    feature_file=os.path.join(output_dir, 'features.log'),
                    select_features=select,
                    result_fields={
                        'chunking': name,
                        'ngrams': seg_name,
                        'selected': str(select) if select is not None else '',
                        },
                )

                for cls, args2 in classify.make_jobs(args):
                    yield Job(
                        cls,
                        args2,
                        name,
                        seg_name,
                        str(select) if select is not None else '',
                    )


def main():
    results_file = os.path.join(OUTPUT, 'results.csv')
    print('writing results to "{}"'.format(results_file))
    if os.path.exists(results_file):
        os.remove(results_file)

    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)

    with open(results_file, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(Result._fields)
        writer.writerows(run_all(DATADIR, OUTPUT, NGRAMS))


if __name__ == '__main__':
    main()
