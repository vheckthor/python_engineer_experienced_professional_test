"""Main Entry point of schema analyzer
"""
from schema_analyzer import generate_schema

INPUT_JSON_PATH = (str(input("Enter the full file path of the input json file: "))
                   or './data/data_2.json')
OUTPUT_FILENAME= (str(input("Enter the full file path of the output json file: "))
                      or 'schema_2')

if __name__ == "__main__":
    generate_schema(INPUT_JSON_PATH, OUTPUT_FILENAME)
