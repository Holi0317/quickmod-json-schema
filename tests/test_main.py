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


class TestMainJson(unittest.TestCase):
    'Tests for index quickmod file'
    def __init__(self, *args, **kwargs):
        'Setup variables'
        super(TestMainJson, self).__init__(*args, **kwargs)

        data_dir = os.path.join(THIS_DIR, 'data/main')

        # Paths of files
        schema = os.path.join(THIS_DIR, '../main.json')

        # With minimal required data
        valid_data_1 = os.path.join(data_dir, 'valid1.json')
        # With some optional data
        valid_data_2 = os.path.join(data_dir, 'valid2.json')

        # Some items got missing url or uid key
        invalid_data_1 = os.path.join(data_dir, 'invalid1.json')
        # Empty index array
        invalid_data_2 = os.path.join(data_dir, 'invalid2.json')

        self.schema = json_load(schema)

        self.valid_data_1 = json_load(valid_data_1)
        self.valid_data_2 = json_load(valid_data_2)

        self.invalid_data_1 = json_load(invalid_data_1)
        self.invalid_data_2 = json_load(invalid_data_2)

    def test_schema_valid(self):
        'Test if schema is valid'
        try:
            Draft4Validator.check_schema(self.schema)
        except SchemaError as error:
            self.fail('main.json got incorrect schema. %s' % error)

    def test_valid_1(self):
        'Test with Minimal, valid data'
        try:
            validate(self.valid_data_1, self.schema)
        except ValidationError as error:
            self.fail('Minimal main.qm data got error. %s' % error)

    def test_valid_2(self):
        'Test with full qm data. Some optional data is still missing'
        try:
            validate(self.valid_data_2, self.schema)
        except ValidationError as error:
            self.fail('Full main.qm data got error. %s' % error)

    def test_invalid_1(self):
        'Data with incorrect formatVersion'
        with self.assertRaisesRegex(ValidationError,
                                    "Failed validating 'enum'"):
            validate(self.invalid_data_1, self.schema)

    def test_invalid_2(self):
        'main.qm without updateUrl key'
        with self.assertRaisesRegex(ValidationError,
                                    "'updateUrl' is a required property"):
            validate(self.invalid_data_2, self.schema)
