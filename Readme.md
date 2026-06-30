# Excel Logic Analyzer

## Overview

Excel Logic Analyzer is a Python desktop application that automatically discovers and explains the business logic connecting two related Excel workbooks.

Instead of simply comparing values, the application reverse-engineers formulas, lookups, relationships, mathematical operations, conditional rules, and dependencies to explain how the target workbook is derived from the source workbook.

---

## Features

- Upload Source and Target Excel files
- Read multiple worksheets
- Workbook summary
- Formula detection
- Lookup detection
- Column mapping using fuzzy matching
- Mathematical relationship discovery
- Conditional business rule detection
- Dependency graph generation
- Confidence score calculation
- PDF report generation
- Excel report generation

---

## Tech Stack

### Language
- Python 3.13+

### GUI
- CustomTkinter

### Libraries
- Pandas
- OpenPyXL
- NumPy
- RapidFuzz
- Scikit-learn
- NetworkX
- Matplotlib
- ReportLab

---

## Project Structure

```text
Excel_Logic_Analyzer/
│
├── app.py
│
├── core/
│
├── gui/
│
├── utils/
│
├── reports/
│
├── uploads/
│
├── assets/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

## Planned Modules

- Excel Reader
- Workbook Analyzer
- Formula Detector
- Column Mapper
- Lookup Detector
- Relationship Detector
- Conditional Rule Detector
- Dependency Graph Generator
- Confidence Engine
- Report Generator

---

## Future Enhancements

- AI-powered rule discovery
- SQL logic detection
- Power BI relationship analysis
- Interactive dependency visualization
- Machine learning-based formula prediction

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/excel-logic-analyzer.git
```

Navigate to the project folder

```bash
cd excel-logic-analyzer
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

## Development Status

Current Phase

- [x] Project Planning
- [ ] Project Setup
- [ ] Excel Reader
- [ ] Workbook Analyzer
- [ ] Formula Detection
- [ ] Column Mapping
- [ ] Lookup Detection
- [ ] Relationship Discovery
- [ ] Conditional Rule Detection
- [ ] Dependency Graph
- [ ] Report Generation
- [ ] Desktop GUI

---

## Author

Developed by Sandhya & Bhoomi
