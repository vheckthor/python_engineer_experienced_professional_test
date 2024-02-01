"""Unit tests for functions in schema_analyzer"""
import unittest
from unittest.mock import Mock, patch, mock_open
from schema_analyzer import analyze_structure, generate_schema

class TestAnalyzeStructure(unittest.TestCase):

    def test_with_simple_dict(self):
        data = {"name": "John", "age": 30}
        result = analyze_structure(data)
        expected = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "tag": "", "description": ""},
                "age": {"type": "integer", "tag": "", "description": ""}
            },
            "required": False,
            "tag": "",
            "description": ""
        }
        self.assertEqual(result["type"], "object")
        self.assertIn("name", result["properties"])
        self.assertIn("age", result["properties"])
        self.assertEqual(result["properties"]["name"]["type"], "string")
        self.assertEqual(result["properties"]["age"]["type"], "integer")
        self.assertDictEqual(result, expected)

    def test_with_array_of_strings(self):
        data = ["red", "green", "blue"]
        result = analyze_structure(data)
        expected = {
            "type": "enum",
            "tag": "",
            "description": ""
        }
        self.assertEqual(result["type"], "enum")
        self.assertDictEqual(analyze_structure(data), expected)

    def test_with_array_of_dicts(self):
        data = [{"id": 1}, {"id": 2}]
        result = analyze_structure(data)
        expected = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "tag": "", "description": ""}
                },
                "required": False,
                "tag": "",
                "description": ""
            },
            "tag": "",
            "description": ""
        }
        self.assertEqual(result["type"], "array")
        self.assertEqual(result["items"]["type"], "object")
        self.assertDictEqual(result, expected)

    def test_with_empty_array(self):
        data = []
        expected = {
            "type": "enum",
            "tag": "",
            "description": ""
        }
        self.assertDictEqual(analyze_structure(data), expected)

    def test_with_boolean(self):
        data = True
        result = analyze_structure(data)
        expected = {
            "type": "boolean",
            "tag": "",
            "description": ""
        }
        self.assertEqual(result["type"], "boolean")
        self.assertDictEqual(result, expected)

    def test_with_integer(self):
        data = 890
        result = analyze_structure(data)
        expected = {
            "type": "integer",
            "tag": "",
            "description": ""
        }
        self.assertEqual(result["type"], "integer")
        self.assertDictEqual(result, expected)

    def test_with_float(self):
        data = 2.12
        result = analyze_structure(data)
        expected = {
            "type": "float",
            "tag": "",
            "description": ""
        }
        self.assertEqual(result["type"], "float")
        self.assertDictEqual(result, expected)

    def test_with_nested_dict(self):
        data = {"user": {"id": "123", "nickname": "JohnDoe"}}
        expected = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "tag": "", "description": ""},
                        "nickname": {"type": "string", "tag": "", "description": ""}
                    },
                    "required": False,
                    "tag": "",
                    "description": ""
                }
            },
            "required": False,
            "tag": "",
            "description": ""
        }
        self.assertEqual(analyze_structure(data), expected)

    def test_with_complex_structure_assert_all_items(self):
        data = {
            "user": {
                "id": "ABCDEFGHIJKLMNOP",
                "nickname": "ABCD"
            },
            "time": 890,
            "acl": [],
            "publicFeed": False,
            "internationalCountries": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZA",
                "ABCDEFGHIJKLMNOPQ"
            ],
            "topTraderFeed": 2.12
        }
        result = analyze_structure(data)
        self.assertEqual(result["type"], "object")
        self.assertIn("user", result["properties"])
        self.assertIn("time", result["properties"])
        self.assertIn("acl", result["properties"])
        self.assertIn("publicFeed", result["properties"])
        self.assertIn("internationalCountries", result["properties"])
        self.assertIn("topTraderFeed", result["properties"])
        self.assertEqual(result["properties"]["publicFeed"]["type"], "boolean")
        self.assertEqual(result["properties"]["internationalCountries"]["type"], "enum")

    def test_with_complex_structure_and_where_root_is_specified(self):
        data = {
            "message": {
                "user": {
                    "id": "ABCDEFGHIJKLMNOP",
                    "nickname": "ABCD",
                    "title": "ABCDEFGHIJKLMNOPQRSTUVWXYZABC",
                    "accountType": "ABCDEFGHIJKLMNOPQRSTUVWX",
                    "countryCode": "ABCDEFGHIJKLMNOPQRSTUVWX",
                    "orientation": "ABCDEFGHIJKLMNOPQRSTU"
                },
                "time": 890,
                "acl": [],
                "publicFeed": False,
                "internationalCountries": [
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZA",
                    "ABCDEFGHIJKLMNOPQ",
                    "ABCDEFGHIJKLMNOPQRSTUVW",
                    "ABCDEFGHIJKLMNOPQRSTUVWXY",
                    "ABCDEFGHIJK",
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "ABCDEFGHIJKLMNOPQR",
                    "ABCDEFG",
                    "ABCDEFGHIJKLM"
                ],
                "topTraderFeed": 2.12
            }
        }
        expected =  {
            "user": {
                "properties": {
                "id": {
                    "type": "string",
                    "tag": "",
                    "description": ""
                },
                "nickname": {
                    "type": "string",
                    "tag": "",
                    "description": ""
                },
                "title": {
                    "type": "string",
                    "tag": "",
                    "description": ""
                },
                "accountType": {
                    "type": "string",
                    "tag": "",
                    "description": ""
                },
                "countryCode": {
                    "type": "string",
                    "tag": "",
                    "description": ""
                },
                "orientation": {
                    "type": "string",
                    "tag": "",
                    "description": ""
                }
                },
                "required": False,
                "type": "object",
                "tag": "",
                "description": ""
            },
            "time": {
                "type": "integer",
                "tag": "",
                "description": ""
            },
            "acl": {
                "type": "enum",
                "tag": "",
                "description": ""
            },
            "publicFeed": {
                "type": "boolean",
                "tag": "",
                "description": ""
            },
            "internationalCountries": {
                "type": "enum",
                "tag": "",
                "description": ""
            },
            "topTraderFeed": {
                "type": "float",
                "tag": "",
                "description": ""
            }
        }
        self.assertDictEqual(analyze_structure(data['message'], True), expected)

    def test_with_complex_structure_and_where_root_is_not_specified(self):
        data = {
            "user": {
                "id": "ABCDEFGHIJKLMNOP",
                "nickname": "ABCD",
                "preferences": {
                    "language": "English",
                    "notifications": True
                }
            },
            "session": {
                "startTime": 1609459200,
                "endTime": 1609462800
            },
            "tags": ["urgent", "new"],
            "isValid": False
        }
        expected = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "tag": "", "description": ""},
                        "nickname": {"type": "string", "tag": "", "description": ""},
                        "preferences": {
                            "type": "object",
                            "properties": {
                                "language": {"type": "string", "tag": "", "description": ""},
                                "notifications": {"type": "boolean", "tag": "", "description": ""}
                            },
                            "required": False,
                            "tag": "",
                            "description": ""
                        }
                    },
                    "required": False,
                    "tag": "",
                    "description": ""
                },
                "session": {
                    "type": "object",
                    "properties": {
                        "startTime": {"type": "integer", "tag": "", "description": ""},
                        "endTime": {"type": "integer", "tag": "", "description": ""}
                    },
                    "required": False,
                    "tag": "",
                    "description": ""
                },
                "tags": {
                    "type": "enum",
                    "tag": "",
                    "description": ""
                },
                "isValid": {
                    "type": "boolean",
                    "tag": "", 
                    "description": ""
                }
            },
            "required": False,
            "tag": "",
            "description": ""
        }
        result = analyze_structure(data)
        self.assertEqual(result["type"], "object")
        self.assertIn("user", result["properties"])
        self.assertEqual(result["properties"]["user"]["type"], "object")
        self.assertIn("preferences", result["properties"]["user"]["properties"])
        self.assertEqual(result["properties"]["user"]["properties"]["preferences"]["type"], "object")
        self.assertIn("tags", result["properties"])
        self.assertEqual(result["properties"]["tags"]["type"], "enum")
        self.assertIn("isValid", result["properties"])
        self.assertEqual(result["properties"]["isValid"]["type"], "boolean")
        self.assertDictEqual(analyze_structure(data), expected)

class TestGenerateSchema(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"message": {"key": "value"}}')
    @patch("schema_analyzer.analyze_structure",
           return_value={'type': 'object', 'properties': {'key': {'type': 'string'}}})
    def test_success_schema_generation(self, mock_analyze, mock_file):
        input_path = "valid_input.json"
        output_path = "output_schema.json"
        generate_schema(input_path, output_path)
        mock_file.assert_called_with(output_path, 'w')
        handle = mock_file()
        self.assertTrue(handle.write.called)

    @patch("builtins.print")
    def test_input_file_not_found(self, mock_print: Mock):
        generate_schema("non_existing_file.json", "output_schema.json")
        called_arg: str = mock_print.call_args[0][0]
        self.assertTrue(called_arg.startswith("An Error occurred: FileNotFoundError"))

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("builtins.print")
    def test_invalid_json_input(self, mock_print: Mock, mock_file):
        generate_schema("invalid_json.json", "output_schema.json")
        called_arg: str = mock_print.call_args[0][0]
        self.assertTrue(called_arg.startswith("An Error occurred: JSONDecodeError"))

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    @patch("schema_analyzer.analyze_structure", return_value={})
    def test_missing_message_field(self, mock_analyze, mock_file):
        input_path = "missing_message.json"
        output_path = "output_schema.json"
        generate_schema(input_path, output_path)
        mock_analyze.assert_called_with({}, True)


if __name__ == '__main__':
    unittest.main()
