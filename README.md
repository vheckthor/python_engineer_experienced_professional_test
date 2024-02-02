

# Python JSON Schema Analyzer

This project provides a tool to analyze JSON schemas, enabling users to input a JSON file and output a schema analysis. It is designed for test purposes, ensuring their the data structure meets expected patterns or specifications.

## Getting Started

Follow these instructions to set up the project locally for development and testing.

### Prerequisites

Ensure you have Python 3.6+ installed on your machine. You can check your Python version by running:

```bash
python --version
```

This project uses standard Python libraries, so no additional installations are required for the basic functionality.

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/vheckthor/python_engineer_experienced_professional_test.git
cd python_engineer_experienced_professional_test
```

### Running the Application

To analyze a JSON schema, `main.py` prompts you for the input and output file paths. You can also use default paths by pressing enter without typing a path.

Run the script:

```bash
python main.py
```

Follow the prompts to enter the full file path of the input JSON file and the filename of the output JSON file. If no path is are enter, the script uses default file in the `./data` and default filename of `schema_2` (`./data/data_2.json` for the input and `schema_2` for the output file name).

### Running the Tests

To ensure the functionality of the JSON schema analyzer, execute the included unit tests with:

```bash
python -m unittest schema_analyzer_test.py
```

This command runs tests defined in `schema_analyzer_test.py`, verifying that the schema analyzer behaves as expected.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

