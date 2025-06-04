# E-commerce Data Pipeline Project

This project contains scripts for processing and analyzing e-commerce data.

## Project Structure

```
ecommerce-pipeline-project/
├── data/               # Directory containing CSV data files
├── extract/           # Data extraction scripts
│   └── extract.py     # Script to analyze CSV files
└── README.md          # This documentation file
```

## Extract Script

The `extract.py` script analyzes CSV files in the `data` directory and provides a summary of their contents.

### Features

- Scans all CSV files in the data directory
- Provides summary statistics for each file:
  - Number of rows
  - Number of columns
  - File name
- Handles errors gracefully if files cannot be read

### Usage

1. Place your CSV files in the `data` directory
2. Run the script:
```bash
python extract/extract.py
```

### Output

The script will display a table showing:
- File name
- Number of rows
- Number of columns
- Any errors encountered while reading the file

Example output format:
```
file_name    num_rows    num_columns
data1.csv    1000       15
data2.csv    500        8
```

### Requirements

- Python 3.x
- pandas library

### Installation

Install the required dependencies:
```bash
pip install pandas
```
