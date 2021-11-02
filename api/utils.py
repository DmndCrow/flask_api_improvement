import os
import sys
import csv

from sqlalchemy.orm import class_mapper


def get_csv_fields():
    return (
        'id', 'name', 'sort_name', 'email', 'twitter', 'facebook',
        'group', 'group_id', 'area_id', 'area', 'chamber', 'term',
        'start_date', 'end_date', 'image', 'gender',
        'wikidata', 'wikidata_group', 'wikidata_area'
    )


def read_csv_file():
    fields = get_csv_fields()

    f = open(os.path.join(os.path.dirname(sys.argv[0]), 'api/gb_parliament.csv'), 'r', newline='')

    reader = csv.DictReader(f, fields)
    data = []

    for i, row in enumerate(reader):
        if i:
            data.append(row)

    return data


def remove_extra_keys(dictionary, model):
    mapper = class_mapper(model)

    mapped_model_keys = {
        k: v for k, v in dictionary.items()
        if k in mapper.attrs.keys()
    }

    return mapped_model_keys
