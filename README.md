# AIC Coordinator Command Centre

A Streamlit prototype for monitoring the AIC Portfolio Challenge.

## Current version

This version covers **Problem Identification** only and uses 50 synthetic records.

## Run locally

1. Install Python 3.11 or later.
2. Open a terminal in this folder.
3. Create a virtual environment:

   Windows:
   `python -m venv .venv`
   `.venv\Scripts\activate`

   macOS/Linux:
   `python3 -m venv .venv`
   `source .venv/bin/activate`

4. Install packages:

   `pip install -r requirements.txt`

5. Run:

   `streamlit run app.py`

6. Open the local URL shown by Streamlit, normally:
   `http://localhost:8501`

## Data

The sample workbook is in `data/synthetic_problem_data.xlsx`.

The app also allows you to upload an Excel/CSV response file from the sidebar.

## Next phase

Replace the sample data with the Google Form response sheet, then add:
- live Google Sheets connection
- faculty/section master mapping
- Progress Tracking
- Evaluation
- Risk engine
- portfolio completion
- viva tracking
