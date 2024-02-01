"""Main Entry point of schema analyzer
"""
from schema_analyzer import generate_schema


# Example usage for testing sake
INPUT_JSON_PATH = (str(input("Enter the full file path of the input json file: "))
                   or './data/data_2.json')
OUTPUT_SCHEMA_PATH = (str(input("Enter the full file path of the output json file: "))
                      or './schema/schema_2.json')

if __name__ == "__main__":
    generate_schema(INPUT_JSON_PATH, OUTPUT_SCHEMA_PATH)
