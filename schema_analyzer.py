"""Functions for analyzing and merging data
"""
import json
from traceback import format_exc

def analyze_structure(data: dict, is_root: bool = False) -> dict:
    """Analyze the JSON structure and return a schema with enhanced type handling."""
    schema = {}
    if isinstance(data, dict):
        properties = {}
        for key, value in data.items():
            # Pass is_root as False for all nested structures
            properties[key] = analyze_structure(value, is_root=False)     
        if not is_root:
            schema = {
                "properties": properties,
                "required": False
            }
            schema.update({
                "type": "object",
                "tag": "",
                "description": ""
            })
        else:
            schema = properties
    elif isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            schema = {
                "type": "enum",
                "tag": "",
                "description": ""
            }
        elif all(isinstance(item, dict) for item in data):
            item_schemas = [analyze_structure(item, is_root=False) for item in data]
            schema = {
                "type": "array",
                "items": item_schemas[0] if item_schemas else {},
                "tag": "",
                "description": ""
            }
        else:
            schema = {
                "type": "array",
                "items": {},
                "tag": "",
                "description": ""
            }
    elif isinstance(data, bool):
        schema = {
            "type": "boolean",
            "tag": "",
            "description": ""
        }
    elif isinstance(data, int):
        schema = {
            "type": "integer",
            "tag": "",
            "description": ""
        }
    elif isinstance(data, float):
        schema = {
            "type": "float",
            "tag": "",
            "description": ""
        }
    else:
        schema = {
            "type": "string",
            "tag": "",
            "description": ""
        }

    return schema

def generate_schema(input_path: str, output_path: str):
    """Generate the Output file containing schemas

    Args:
        input_path (str): input file path
        output_path (str): output file path
    """
    try:
        with open(input_path, 'r') as file:
            data = json.load(file)
    except (FileExistsError, FileNotFoundError, json.JSONDecodeError) as e:
        error_message = format_exc()
        print(f"An Error occurred: {type(e).__name__} => {error_message}")
        return
    message_data = data.get('message', {})

    schema = analyze_structure(message_data, True)
    with open(output_path, 'w') as file:
        json.dump(schema, file, indent=2)
    print(f"Operation successful find the output file here => {output_path}")
