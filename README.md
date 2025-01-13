# Keyword Volume Analyzer

A Streamlit application that helps you get search volume data for your keywords using the Keywords Everywhere API.

## Features

- Upload Keywords Everywhere API key securely
- Import keywords from CSV file
- Get search volume, CPC, and competition data for keywords
- Download results as CSV
- Handles up to 100 keywords per API request
- User-friendly interface

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## How to Use

1. Get your API key from Keywords Everywhere
2. Launch the application
3. Enter your API key in the secure input field
4. Upload a CSV file containing your keywords (one keyword per row)
5. Click "Get Keyword Data" to fetch the results
6. Download the results as a CSV file

## CSV File Format

Your CSV file should contain keywords in the first column. The column header name doesn't matter.

Example:
```
keywords
digital marketing
seo services
web design
```

## Security Note

Your API key is handled securely and is never stored or logged by the application.
