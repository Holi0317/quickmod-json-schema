#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test if index.json will validate correct json file.
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

        data_dir = os.path.join(THIS_DIR, 'data/index')

        # Paths of files
        schema = os.path.join(THIS_DIR, '../index.json')

        # Without optional data
        valid_data_1 = os.path.join(data_dir, 'valid1.json')
        # With optional data, baseUrl
        valid_data_2 = os.path.join(data_dir, 'valid2.json')

        # Some items got missing url or uid key
        invalid_data_1 = os.path.join(data_dir, 'invalid1.json')
        # Empty index array
        invalid_data_2 = os.path.join(data_dir, 'invalid2.json')
        # Totally irrelevant data
        invalid_data_3 = os.path.join(data_dir, 'invalid3.json')

        self.schema = json_load(schema)

        self.valid_data_1 = json_load(valid_data_1)
        self.valid_data_2 = json_load(valid_data_2)

        self.invalid_data_1 = json_load(invalid_data_1)
        self.invalid_data_2 = json_load(invalid_data_2)
        self.invalid_data_3 = json_load(invalid_data_3)

    def test_schema_valid(self):
        'Test if schema is valid'
        try:
            Draft4Validator.check_schema(self.schema)
        except SchemaError as error:
            self.fail('Index.json got incorrect schema. %s' % error)

    def test_valid_1(self):
        'Minimal, valid data test'
        try:
            validate(self.valid_data_1, self.schema)
        except ValidationError as error:
            self.fail('Minimal index.qm got error. %s' % error)

    def test_valid_2(self):
        'Valid data with optional data, baseUrl'
        try:
            validate(self.valid_data_2, self.schema)
        except ValidationError as error:
            self.fail('index.qm with baseUrl got error. %s' % error)

    def test_invalid_1(self):
        'Some item got missing url or uid key'
        with self.assertRaises(ValidationError):
            validate(self.invalid_data_1, self.schema)

    def test_invalid_2(self):
        'Data with empty index array'
        with self.assertRaises(ValidationError):
            validate(self.invalid_data_2, self.schema)

    def test_invalid_3(self):
        'Totally irrelevant json data'
        with self.assertRaises(ValidationError):
            validate(self.invalid_data_3, self.schema)
