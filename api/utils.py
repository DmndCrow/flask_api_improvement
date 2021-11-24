import os
import sys
import csv

from sqlalchemy.orm import class_mapper
from sqlalchemy import inspect


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


def remove_extra_keys(dictionary, model, original=None):
    mapper = class_mapper(model)

    mapped_model_keys = {
        k: v for k, v in dictionary.items()
        if k in mapper.attrs.keys()
    }

    inst = inspect(model)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    for key in attr_names:
        if key not in mapped_model_keys:
            mapped_model_keys[key] = ''

    if original:
        for key in attr_names:
            if key not in dictionary:
                mapped_model_keys[key] = original[key]

    return model(**mapped_model_keys)
