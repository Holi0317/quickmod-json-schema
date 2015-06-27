#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test if main.json will validate json file correctly.
'''

import unittest
import json
import os

from jsonschema import validate, Draft4Validator
from jsonschema.exceptions import ValidationError, SchemaError

from . import __file__ as test_directory


THIS_DIR = os.path.dirname(test_directory)


def json_load(file_path):
    'Open, load and close json file wrapper'
    with open(file_path, 'r') as file:
        content = json.loads(file.read())
    return content


class TestIndexJson(unittest.TestCase):
    'Tests for index quickmod file'
    def __init__(self, *args, **kwargs):
        'Setup variables'
        super(TestIndexJson, self).__init__(*args, **kwargs)

        data_dir = os.path.join(THIS_DIR, 'data/main')

        # Paths of files
        schema = os.path.join(THIS_DIR, '../main.json')

        # Without optional data
        valid_data = os.path.join(data_dir, 'valid1.json')
        # With some optional data
        valid_data_optional = os.path.join(data_dir, 'valid2.json')

        # Some items got missing url or uid key
        invalid_data = os.path.join(data_dir, 'invalid1.json')
        # Empty index array
        invalid_data_empty_index = os.path.join(data_dir, 'invalid2.json')

        self.schema = json_load(schema)
        self.valid_datas = [json_load(valid_data),
                            json_load(valid_data_optional)]
        self.invalid_datas = [json_load(invalid_data),
                              json_load(invalid_data_empty_index)]

    def test_schema_valid(self):
        'Test if schema is valid'
        try:
            Draft4Validator.check_schema(self.schema)
        except SchemaError as error:
            self.fail('Index.json got incorrect schema. %s' % error)

    def test_valid(self):
        'If valid data is passed in, no exception should be raised'
        # If exception raised, fail this test
        try:
            for data in self.valid_datas:
                validate(data, self.schema)
        except ValidationError as error:
            self.fail('Correct qm index data got error. %s' % error)

    def test_incorrect_data(self):
        'If invalid data is passed in, ValidationError should be raised'
        with self.assertRaises(ValidationError):
            for data in self.invalid_datas:
                validate(data, self.schema)
