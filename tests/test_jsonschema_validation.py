# -*- coding: utf-8 -*-
# This file is part of https://github.com/26fe/jsonstat.py
# Copyright (C) 2016 gf <gf@26fe.com>
# See LICENSE file

# stdlib
from __future__ import print_function
# from __future__ import unicode_literals
import os
import unittest
import json

# packages
import jsonschema

# jsonstat
import jsonstat
import jsonstat.schema as JS_SCHEMA


class TestJsonSchemaValidation(unittest.TestCase):
    def setUp(self):
        self.fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    def test_dimension(self):
        # dimension.index as array
        jsonstat_dimension = {
            "label": "sex",
            "category":
                {
                    "index": ["M", "F", "T"],
                    "label": {
                        "M": "men",
                        "F": "women",
                        "T": "total"
                    }
                }
        }
        try:
            jsonschema.validate(jsonstat_dimension, JS_SCHEMA.dimension)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dimension.child
        jsonstat_dimension = {
            "label": "activity status",
            "category": {
                "index": {
                    "A": 0,
                    "E": 1,
                    "U": 2,
                    "I": 3,
                    "T": 4
                },
                "label": {
                    "A": "active population",
                    "E": "employment",
                    "U": "unemployment",
                    "I": "inactive population",
                    "T": "population 15 years old and over"
                },
                "child": {
                    "A": ["E", "U"],
                    "T": ["A", "I"]
                }
            }
        }
        try:
            jsonschema.validate(jsonstat_dimension, JS_SCHEMA.dimension)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dimension.coordinates
        jsonstat_dimension = {
            "category": {
                "label": {
                    "ISO-3166-2:TV": "Tuvalu"
                },
                "coordinates": {
                    "ISO-3166-2:TV": [179.1995, -8.5199]
                }
            }
        }
        try:
            jsonschema.validate(jsonstat_dimension, JS_SCHEMA.dimension)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        json_string = '''
        {
            "label" : "concepts",
            "category" : {
                "index" : {
                    "POP" : 0,
                    "PERCENT" : 1
                },
                "label" : {
                    "POP" : "population",
                    "PERCENT" : "weight of age group in the population"
                },
                "unit" : {
                    "POP" : {
                        "label": "thousands of persons",
                        "decimals": 1,
                        "type" : "count",
                        "base" : "people",
                        "multiplier" : 3
                    },
                    "PERCENT" : {
                        "label" : "%",
                        "decimals": 1,
                        "type" : "ratio",
                        "base" : "per cent",
                        "multiplier" : 0
                    }
                }
            }
        }'''
        jsonstat_dimension = json.loads(json_string)
        try:
            jsonschema.validate(jsonstat_dimension, JS_SCHEMA.dimension)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

    def test_dataset(self):
        jsonstat_dataset = {
            "version": "2.0",
            "class": "dataset",
            "label": "Unemployment rate in the OECD countries 2003-2014",
            "source": "Economic Outlook No 92 - December 2012 - OECD Annual Projections",
            "updated": "2012-11-27",
            "id": ["concept", "area", "year"],
            "size": [1, 36, 12],
            "dimension": {},
            "value": []
        }

        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.role
        jsonstat_dataset = {
            "version": "2.0",
            "class": "dataset",
            "id": ["concept", "arrival_date", "departure_date", "origin", "destination"],
            "size": [1, 24, 24, 10, 10],
            "role": {
                "time": ["arrival_date", "departure_date"],
                "geo": ["origin", "destination"],
                "metric": ["concept"]
            }}

        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.value null value
        json_string = """{
            "version": "2.0",
            "class": "dataset",
            "value": [105.3, 104.3, null, 177.2]
            }
        """
        jsonstat_dataset3 = json.loads(json_string)
        # print(self.jsonstat_dataset3)
        try:
            jsonschema.validate(jsonstat_dataset3, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.value as dict
        jsonstat_dataset = {
            "version": "2.0",
            "class": "dataset",
            "value": {"0": 1.3587, "18": 1.5849},
        }
        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.status
        json_string = """{
            "version": "2.0",
            "class": "dataset",
            "value": [100, null, 102, 103, 104],
            "status": ["a", "m", "a", "a", "p"]
        }"""
        jsonstat_dataset = json.loads(json_string)
        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.status
        jsonstat_dataset6 = {
            "version": "2.0",
            "class": "dataset",
            "value": [100, 99, 102, 103, 104],
            "status": "e",
        }
        try:
            jsonschema.validate(jsonstat_dataset6, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.status
        jsonstat_dataset7 = json.loads("""{
            "version": "2.0",
            "class": "dataset",
            "value": [100, null, 102, 103, 104],
            "status": {"1": "m"}
        }""")

        try:
            jsonschema.validate(jsonstat_dataset7, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.dimension
        jsonstat_dataset = {
            "version": "2.0",
            "class": "dataset",
            "value": [100, 99, 102, 103, 104],
            "status": "e",
            "dimension": {
                "metric": {},
                "time": {},
                "geo": {},
                "sex": {},

            }
        }
        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        # dataset.link
        jsonstat_dataset = {
            "version": "2.0",
            "class": "dataset",
            "link": {
                "alternate": [
                    {
                        "type": "text/csv",
                        "href": "http://provider.domain/2002/population/sex.csv"
                    },
                    {
                        "type": "text/html",
                        "href": "http://provider.domain/2002/population/sex.html"
                    }
                ]}}

        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

    def test_collection_complete(self):

        # json_string = '{"uffa":false}'
        # json_data = json.loads(json_string)
        # print(json_data)

        jsonstat_dimension_sex = {
            "label": "sex",
            "category":
                {
                    "index": {"M": 0, "F": 1, "T": 2},
                    "label": {
                        "M": "men",
                        "F": "women",
                        "T": "total"
                    }
                }
        }

        jsonstat_dataset = {"label": "boh",
                            "dimension": {"sex": jsonstat_dimension_sex}}

        jsonstat_collection = {
            "version": "2.0",
            "class": "collection",
            "href": "http://json-stat.org/samples/oecd-canada-col.json",
            "label": "OECD-Canada Sample Collection",
            "updated": "2015-12-24",
            "link": {
                "item": [jsonstat_dataset]
            }
        }
        try:
            jsonschema.validate(jsonstat_dimension_sex, JS_SCHEMA.dimension)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        try:
            jsonschema.validate(jsonstat_dataset, JS_SCHEMA.dataset)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        try:
            jsonschema.validate(jsonstat_collection, JS_SCHEMA.collection)
        except jsonschema.exceptions.SchemaError as e:
            self.fail("validate failed!")

        self.assertTrue(jsonstat.validate(jsonstat_collection))

    def test_validate(self):
        fixture_jsonstat_org_dir = os.path.join(self.fixture_dir, "json-stat.org")
        for f in os.listdir(fixture_jsonstat_org_dir):
            jsonstat_file = os.path.join(fixture_jsonstat_org_dir, f)
            if os.path.isfile(jsonstat_file) and jsonstat_file.endswith(".json"):
                # print("validating {}".format(jsonstat_file))
                with open(jsonstat_file) as f:
                    json_string = f.read()
                    try:
                        ret = jsonstat.validate(json_string)
                        msg = "validating {}".format(jsonstat_file)
                        self.assertTrue(ret, msg)
                    except jsonstat.JsonStatException:
                        pass

if __name__ == '__main__':
    unittest.main()
