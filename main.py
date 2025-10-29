import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO
import gspread
import gspread_formatting as gfmt
import google.generativeai as genai
import json

# ============ CONFIGURATION ============
GOOGLE_SHEET_NAME = "Daily Work Log" 
WORKSHEET_NAME = "Sheet1"
# ---------------------------------

# ============ PAGE SETUP ============
st.set_page_config(page_title="📊 AI Daily Work Logger", layout="wide")

# ============ CUSTOM CSS FOR STYLING ============
def load_css(file_name):
    """Function to load a local CSS file."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Don't show an error, just a warning in the console or log if needed
        pass

# Load the custom CSS
load_css("style.css")


# ============ GOOGLE SHEETS CONNECTION ============

@st.cache_resource
def connect_to_google_sheets():
    """Establish a connection to the Google Sheet."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        
        client = gspread.service_account_from_dict(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
        
        try:
            spreadsheet = client.open(GOOGLE_SHEET_NAME)
        except gspread.SpreadsheetNotFound:
            st.error(f"❌ **Spreadsheet Not Found:** Could not find a Google Sheet named **'{GOOGLE_SHEET_NAME}'**.")
            st.error("Please check the `GOOGLE_SHEET_NAME` variable in your code and ensure you have shared the sheet with your service account's email.")
            return None
        except Exception as e:
            st.error(f"❌ Error opening spreadsheet: {e}")
            return None

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

# ============ AI (GEMINI) INTEGRATION ============

@st.cache_resource
def get_gemini_model():
    """Initializes and returns a cached Gemini model instance."""
    try:
        gemini_key = st.secrets["gemini_api_key"]
        genai.configure(api_key=gemini_key)
        
        # Define the system instruction for the LLM
        system_instruction = (
            "You are an expert assistant for logging daily work. The user will provide a natural language summary "
            "of their day. Your job is to extract one or more tasks from this summary. "
            "For each task, you must identify three pieces of information: "
            "1. 'project_category': The project or main topic (e.g., 'PII Detection', 'Team Meeting', 'General'). "
            "2. 'accomplishment': A concise summary of the specific task or accomplishment. "
            "3. 'key_insight': An insight, outcome, or blocker related to the accomplishment. "
            "If no specific insight is mentioned, infer one or state 'N/A'. "
            "Always respond with a valid JSON array of task objects, even if you only find one task. "
            "Do not return an empty array unless the input is completely blank or irrelevant."
        )
        
        # Define the JSON schema we want the LLM to return
        response_schema = {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "project_category": { "type": "STRING" },
                    "accomplishment": { "type": "STRING" },
                    "key_insight": { "type": "STRING" }
                },
                "required": ["project_category", "accomplishment", "key_insight"]
            }
        }

        # Set up the model generation config
        generation_config = {
            "response_mime_type": "application/json",
            "response_schema": response_schema,
            "temperature": 0.2
        }

        # Create the model instance
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-preview-09-2025",
            system_instruction=system_instruction,
            generation_config=generation_config
        )
        return model
    except Exception as e:
        st.error(f"❌ **Gemini AI Error:** Could not initialize the AI model. Check your `gemini_api_key` in Streamlit Secrets. Details: {e}")
        return None

def call_gemini_to_parse_summary(summary_text, model):
    """
    Calls the Gemini API to parse the summary and returns a list of task dicts.
    """
    if not model:
        return None
        
    try:
        with st.spinner("Logger is analyzing your summary..."):
            response = model.generate_content(summary_text)
            task_list = json.loads(response.text)
            return task_list
    except Exception as e:
        st.error(f"❌ **AI Parsing Error:** The AI model had trouble understanding the input. Details: {e}")
        st.error("Please try rephrasing your summary.")
        return None

# ============ HELPER FUNCTIONS (FROM YOUR CODE) ============

def apply_gsheet_formatting(worksheet):
    """
    Applies formatting to the Google Sheet header and auto-resizes columns.
    """
    try:
        # Define the header format
        header_format = gfmt.CellFormat(
            backgroundColor=gfmt.Color(0.91, 0.96, 0.99), # Light blue
            textFormat=gfmt.TextFormat(bold=True, foregroundColor=gfmt.Color(0.05, 0.28, 0.63)), # Dark blue
            horizontalAlignment='CENTER'
        )
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
        st.warning(f"Could not apply some formatting to Google Sheet. Data was still saved. Error: {e}")


def save_data_to_gsheet(df_new, worksheet):
    """
    Append new data to the specified Google Sheet worksheet.
    - Checks if the sheet is empty to add headers.
    - Applies formatting after saving.
    """
    try:
        list_of_lists = worksheet.get_all_values()
        
        rows_to_append = []
        is_empty_sheet = not list_of_lists
        
        if is_empty_sheet:
            st.info("Sheet was empty. Writing headers...")
            headers = df_new.columns.tolist()
            rows_to_append.append(headers)
        
        rows_to_append.extend(df_new.values.tolist())
        
        st.info(f"Appending {len(rows_to_append)} row(s) to Google Sheet...")
        worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
            
        st.success(f"Saved {len(df_new)} new record(s) to Google Sheet: **{GOOGLE_SHEET_NAME}**")
        
        apply_gsheet_formatting(worksheet)

    except Exception as e:
        st.error(f"❌ An unexpected error occurred while **saving data**: {e}")
        st.error("This can happen if the data format doesn't match the sheet or due to permissions issues.")


# ============ UI & MAIN LOGIC ============
st.title("Daily Work Logger")
st.markdown("Write your daily work summary in plain English. I will parse it and save it to your Google Sheet.")

# Attempt to connect to Google Sheets and get AI Model
worksheet = connect_to_google_sheets()
gemini_model = get_gemini_model()

# Only show the rest of the app if the connection was successful
if worksheet and gemini_model:
    
    # These are the *exact* column names in your Google Sheet
    sheet_columns = ["Date", "Project / Category", "Accomplishment", "Key Insight / Outcome"]

    with st.expander("📘 How to Use & Example Format", expanded=False):
        st.markdown(f"""
        **1. Write Your Summary:** Type what you did today in the text box.
        
        **2. Be Descriptive:** The more detail you give, the better the AI can parse it.
        
        **Example Input:**
        > "Today was focused on the PII Detection project. I validated the package for 5 countries, and the main outcome was that the package is stable, but I found a new false-positive. Also had a team meeting about the Q4 roadmap."

        **Example AI Output (Saved to Sheet):**
        | Date | Project / Category | Accomplishment | Key Insight / Outcome |
        |---|---|---|---|
        | 2025-10-29 | PII Detection | Validated package for 5 countries | Package is stable, but found new false-positive |
        | 2025-10-29 | Team Meeting | Discussed Q4 roadmap | N/A |

        **3. Click Save!** Your data will be analyzed, parsed, and appended to your Google Sheet.
        """)

    if "summary_input" not in st.session_state:
        st.session_state.summary_input = ""

    summary_input = st.text_area(
        "**Enter your daily work summary:**",
        value=st.session_state.summary_input,
        height=200,
        key="summary_input_area",
        placeholder="Today I worked on Project X, finished the Y feature, and had a meeting about Z..."
    )

    if st.button("Log My Day", type="primary"):
        if not summary_input.strip():
            st.warning("Please write a summary before saving.")
        else:
            try:
                # 1. Call the LLM to parse the summary
                task_list = call_gemini_to_parse_summary(summary_input, gemini_model)
                
                if not task_list:
                    st.error("❌ **AI Error:** The AI could not extract any tasks. Please try again.")
                    st.stop()

                # 2. Convert the list of tasks (dicts) into a DataFrame
                df_new = pd.DataFrame(task_list)

                if df_new.empty:
                    st.error("❌ **Data Error:** The AI returned an empty list. Please check your summary and try again.")
                else:
                    # 3. Add the 'Date' column
                    today = datetime.now().strftime("%Y-%m-%d")
                    df_new.insert(0, "Date", today)
                    
                    # 4. Rename AI-friendly keys to match your Sheet's columns
                    df_new = df_new.rename(columns={
                        'project_category': 'Project / Category',
                        'accomplishment': 'Accomplishment',
                        'key_insight': 'Key Insight / Outcome'
                    })
                    
                    # 5. Ensure column order matches the sheet (in case AI adds extra keys)
                    df_new = df_new[sheet_columns]
                    
                    # 6. Ensure all data is string to avoid API errors
                    df_new = df_new.astype(str)
                    
                    # 7. Save to Google Sheets (using your existing function)
                    save_data_to_gsheet(df_new, worksheet)
                    
                    st.markdown("---")
                    st.subheader("AI-Parsed Data (Added to Sheet):")
                    st.dataframe(df_new, use_container_width=True, hide_index=True)
                    
                    st.session_state.summary_input = ""
                    st.rerun()

            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
