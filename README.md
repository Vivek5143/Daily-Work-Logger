<<<<<<< HEAD
📝 Daily AI Work Logger
=======
# 📝 Daily Work Logger
>>>>>>> 4c74e68d9aaefd035eafc1a1c56b91d3caec70b8

A beautiful Streamlit web application, powered by the Gemini AI API, for logging daily work activities directly to Google Sheets. Track your projects, learnings, and improvements simply by writing a summary of your day.

✨ Features

🧠 Natural Language Input: No need to format CSVs. Just write what you did (e.g., "Today I finished the homepage for the 'X' project. It's now live.")

✨ AI-Powered Parsing: Uses the Gemini AI to intelligently extract and categorize your tasks into columns.

🎨 Beautiful UI with custom CSS styling.

📊 Google Sheets Integration: Automatically appends your work log as new rows in a specified Google Sheet.

🔄 Real-time Updates: See your parsed data immediately before saving.

🚀 Quick Start

Prerequisites

Python 3.8 or higher

Google Cloud Project with Sheets API and Drive API enabled

A Gemini API Key from Google AI Studio

Google Service Account with proper permissions

Installation

Clone the repository

git clone [https://github.com/Vivek5143/Daily-Work-Logger.git](https://github.com/Vivek5143/Daily-Work-Logger.git)
cd Daily-Work-Logger


Install dependencies

pip install -r requirements.txt


Set up your credentials in .streamlit/secrets.toml

Create a folder named .streamlit in your project directory.

Create a file inside it named secrets.toml.

Copy the structure from the "Configuration" section below and fill in your actual credentials for both the gemini_api_key and the gcp_service_account.

Share your Google Sheet

Create a Google Sheet named "Daily Work Log" (or whatever you set in the app).

Share it with your service account email (found in your credentials) and give it "Editor" permissions.

Run the application
Make sure your gemini_logger_app.py file is named main.py if you use this command.

streamlit run main.py


📋 Usage

The app now accepts natural language. The old CSV format is no longer needed.

Write Your Summary: In the text area, write a few sentences about what you accomplished. The AI is trained to look for projects, accomplishments, and insights/blockers.

Click "Parse Work Log": The AI will process your text and show you a preview of the structured data it extracted.

Save to Sheet: If the preview looks good, click "Save to Google Sheet" to log your work.

Example Input

Today was all about the new user dashboard. I finished the main layout with the new charting library.
I also had a meeting about the Q4 roadmap, which helped clarify our goals.
The only blocker is that I'm still waiting on the final API endpoints from the backend team.


AI-Parsed Output

Date

Project / Category

Accomplishment

Key Insight / Blocker

2025-10-29

User Dashboard

Finished main layout with new charting library



2025-10-29

Q4 Roadmap

Meeting clarified goals



2025-10-29

Backend API



Waiting on final API endpoints from the backend team.

🔧 Configuration

Environment Variables (.streamlit/secrets.toml)

Create .streamlit/secrets.toml and add your keys:

# Your key from Google AI Studio
gemini_api_key = "...your...gemini...api...key"

# Your Google Cloud Service Account credentials
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_GOES_HERE
-----END PRIVATE KEY-----"""
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "[https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com](https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com)"


Customization

Styling: Edit style.css to customize the appearance.

Sheet Name: Change the sheet name in your Python app file:

GOOGLE_SHEET_NAME = "Your Custom Sheet Name"

<<<<<<< HEAD

🔒 Security

Never commit your secrets.toml file to version control. (Use the .gitignore file!)

Limit service account permissions to only what's needed.

🐛 Troubleshooting

Common Issues

Gemini AI Error / Key not found

Ensure your gemini_api_key is correctly added to secrets.toml as a top-level key.

Make sure your secrets.toml file is in the .streamlit folder.

You must fully restart Streamlit (Ctrl+C and streamlit run...) after changing secrets.

"Spreadsheet not found"

Verify the GOOGLE_SHEET_NAME in the script matches your sheet exactly.

Check that your sheet is shared with the client_email from your service account.

"Permission denied" / "Incorrect padding"

Ensure your service account has "Editor" permissions on the sheet.

Check that the private_key in secrets.toml is copied correctly, using the """...""" multiline format.

🤝 Contributing

Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

📄 License

This project is licensed under the MIT License.

🙏 Acknowledgments

Built with Streamlit

AI parsing by Google's Gemini API

Google Sheets integration via gspread

Happy logging! 📝✨
=======
>>>>>>> 4c74e68d9aaefd035eafc1a1c56b91d3caec70b8
