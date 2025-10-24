import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO
import gspread
# Removed: from google.oauth2.service_account import Credentials
import gspread_formatting as gfmt

# ============ CONFIGURATION ============
# --- FIXED: Removed invisible character from "Daily Work Log" ---
GOOGLE_SHEET_NAME = "Daily Work Log" 
WORKSHEET_NAME = "Sheet1"
# ---------------------------------

# ============ PAGE SETUP ============
st.set_page_config(page_title="📊 Daily Work Logger (Google Sheets)", page_icon="📊", layout="wide")

# ============ CUSTOM CSS FOR STYLING ============
def load_css(file_name):
    """Function to load a local CSS file."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

# Load the custom CSS
load_css("style.css")


# ============ GOOGLE SHEETS CONNECTION ============

@st.cache_resource
def connect_to_google_sheets():
    """Establish a connection to the Google Sheet."""
    try:
        # Scopes for the Google Sheets API
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        # Use the modern gspread service_account_from_dict method
        client = gspread.service_account_from_dict(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
        
        # 1. Try to open the spreadsheet
        try:
            spreadsheet = client.open(GOOGLE_SHEET_NAME)
        except gspread.SpreadsheetNotFound:
            st.error(f"❌ **Spreadsheet Not Found:** Could not find a Google Sheet named **'{GOOGLE_SHEET_NAME}'**.")
            st.error("Please check the `GOOGLE_SHEET_NAME` variable in your code and ensure you have shared the sheet with your service account's email.")
            return None
        except Exception as e:
            st.error(f"❌ Error opening spreadsheet: {e}")
            return None

        # 2. Try to open the specific worksheet (tab)
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
            return worksheet
        except gspread.WorksheetNotFound:
            st.error(f"❌ **Worksheet Not Found:** Found the spreadsheet, but could not find a worksheet tab named **'{WORKSHEET_NAME}'**.")
            st.error("Please check the `WORKSHEET_NAME` variable in your code. It is case-sensitive!")
            return None
        except Exception as e:
            st.error(f"❌ Error opening worksheet: {e}")
            return None

    except Exception as e:
        st.error(f"❌ **Connection Error:** Could not connect to Google Sheets. Please ensure your `secrets.toml` is configured correctly. Details: {e}")
        return None

# ============ HELPER FUNCTIONS ============

def apply_gsheet_formatting(worksheet):
    """
    Applies formatting to the Google Sheet header and auto-resizes columns.
    """
    try:
        st.info("Applying Google Sheet formatting (colors, sizing)...")
        
        # Define the header format
        header_format = gfmt.CellFormat(
            backgroundColor=gfmt.Color(0.91, 0.96, 0.99), # Light blue
            textFormat=gfmt.TextFormat(bold=True, foregroundColor=gfmt.Color(0.05, 0.28, 0.63)), # Dark blue
            horizontalAlignment='CENTER'
        )
        
        # Apply header format to row 1 (A1:D1 for 4 columns)
        gfmt.format_cell_range(worksheet, 'A1:D1', header_format)
        
        # Auto-resize columns A through D
        worksheet.spreadsheet.batch_update({
            "requests": [
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": worksheet.id,
                            "dimension": "COLUMNS",
                            "startIndex": 0,  # Column A
                            "endIndex": 4   # Column D
                        }
                    }
                }
            ]
        })
    except Exception as e:
        st.warning(f"⚠️ Could not apply some formatting to Google Sheet. Data was still saved. Error: {e}")


def save_data_to_gsheet(df_new, worksheet):
    """
    Append new data to the specified Google Sheet worksheet.
    - Checks if the sheet is empty to add headers.
    - Applies formatting after saving.
    """
    try:
        # Get all data to check if the sheet is empty
        list_of_lists = worksheet.get_all_values()
        
        rows_to_append = []
        is_empty_sheet = not list_of_lists
        
        # If the sheet is empty (no headers, no data)
        if is_empty_sheet:
            st.info("Sheet was empty. Writing headers...")
            # Add the header row first
            headers = df_new.columns.tolist()
            rows_to_append.append(headers)
        
        # Add the new data rows
        rows_to_append.extend(df_new.values.tolist())
        
        # Append all new rows (either just data, or headers + data)
        st.info(f"Appending {len(rows_to_append)} row(s) to Google Sheet...")
        worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
            
        st.success(f"✅ Saved {len(df_new)} new record(s) to Google Sheet: **{GOOGLE_SHEET_NAME}**")
        
        # Apply formatting after saving
        apply_gsheet_formatting(worksheet)

    except Exception as e:
        st.error(f"❌ An unexpected error occurred while **saving data**: {e}")
        st.error("This can happen if the data format doesn't match the sheet or due to permissions issues.")


# ============ UI & MAIN LOGIC ============
st.title("📊 Daily Work Logger (Connected to Google Sheets)")
st.markdown("Paste your daily work log in CSV format. The app will automatically save it to your Google Sheet.")

# Attempt to connect to Google Sheets
worksheet = connect_to_google_sheets()

# Only show the rest of the app if the connection was successful
if worksheet:
    # --- MOVED COLUMN DEFINITIONS HERE ---
    cols_4 = ["Date", "Project / Category", "Accomplishment", "Key Insight / Outcome"]
    cols_3 = ["Project / Category", "Accomplishment", "Key Insight / Outcome"]
    # --- END OF MOVE ---

    with st.expander("📘 How to Use & Example Format", expanded=False):
        st.markdown(f"""
        **1. Paste Your Data:** Paste one or more lines of comma-separated values into the text box below.
        
        **2. Format (3 or 4 Columns):** This format is designed to be useful for your final internship report.
        
        **4-Column Format (Date included):**
        `2025-10-24,PII Detection,"Validated package for 5 countries","Package is stable, but found new false-positive"`

        **3-Column Format (Date auto-added):**
        `PII Detection,"Validated package for 5 countries","Package is stable, but found new false-positive"`

        **3. Click Save!** Your data will be appended to your Google Sheet named **"{GOOGLE_SHEET_NAME}"**.
        """)

    if "csv_input" not in st.session_state:
        st.session_state.csv_input = ""

    # Updated placeholder text
    csv_input = st.text_area(
        "✍️ **Paste your CSV line(s) here (3 or 4 columns):**",
        value=st.session_state.csv_input,
        height=200,
        key="csv_input_area",
        placeholder="Project / Category,Accomplishment,Key Insight / Outcome"
    )

    if st.button("💾 Save to Google Sheet", type="primary"):
        if not csv_input.strip():
            st.warning("⚠️ Please paste some data before saving.")
        else:
            try:
                data_io = StringIO(csv_input)
                
                # Read CSV without headers to check column count
                df_new = pd.read_csv(data_io, header=None, dtype=str).fillna("")
                num_cols = len(df_new.columns)

                # --- UPDATED COLUMN NAMES ---
                # (Now defined above)
                # --- END OF UPDATE ---

                if num_cols == 4:
                    # 4 columns provided, assume Date is included
                    df_new.columns = cols_4
                elif num_cols == 3:
                    # 3 columns provided, assume Date is missing
                    df_new.columns = cols_3
                    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    df_new.insert(0, "Date", today)
                else:
                    st.error(f"❌ **Column Error:** Expected 3 or 4 columns, but found {num_cols}. Please check your pasted data.")
                    st.stop() # Stop execution if columns don't match
                
                # Check for empty or malformed data
                if df_new.empty or df_new['Project / Category'].isnull().all():
                    st.error("❌ **Data Error:** The pasted data appears to be empty or in the wrong format. Please check your CSV.")
                else:
                    # Ensure all data is string to avoid API errors
                    df_new = df_new.astype(str)
                    save_data_to_gsheet(df_new, worksheet)
                    
                    st.markdown("---")
                    st.subheader("📊 Recently Added:")
                    st.dataframe(df_new, use_container_width=True, hide_index=True)
                    
                    st.session_state.csv_input = ""
                    st.rerun()

            except pd.errors.ParserError as e:
                st.error(f"❌ **CSV Parsing Error:** Could not read the data.")
                st.error("Please ensure each row has **3 or 4 columns**.")
                st.error(f"*Details: {e}*")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
