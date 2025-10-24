# 📝 Daily Work Logger

A beautiful Streamlit web application for logging daily work activities directly to Google Sheets. Track your projects, learnings, and improvements with an intuitive interface.

## ✨ Features

- 🎨 **Beautiful UI** with custom CSS styling
- 📊 **Google Sheets Integration** - automatically saves to your spreadsheet
- 📝 **Flexible Input** - supports multi-column formats
- 🔄 **Real-time Updates** - see your data immediately
- 🎯 **Easy to Use** - just paste your data and click save

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Sheets API and Drive API enabled
- Google Service Account with proper permissions

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vivek5143/daily-work-logger.git
   cd daily-work-logger
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets credentials**
   - Create a Google Cloud Project
   - Enable Google Sheets API and Google Drive API
   - Create a Service Account
   - Download the JSON credentials
   - Copy `secrets.toml.example` to `.streamlit/secrets.toml`
   - Fill in your actual credentials

4. **Share your Google Sheet**
   - Create a Google Sheet named "Daily Work Log"
   - Share it with your service account email (Editor permissions)

5. **Run the application**
   ```bash
   streamlit run main.py
   ```
   
   Or use the batch file:
   ```bash
   run_logger.bat
   ```

## 📋 Usage

### Input Format

The app accepts CSV data in two formats:

**3 Columns (Date will be added automatically):**
```
Project Name, What I Learned, What Needs Improvement
```

**4 Columns (Date included):**
```
Date, Project Name, What I Learned, What Needs Improvement
```

### Example Data

```
AI Development, Built a chatbot, Need to improve error handling
Data Analysis, Created visualizations, Learn more about statistics
Web Design, Improved UI/UX, Practice responsive design
```

## 🔧 Configuration

### Google Sheets Setup

1. **Create a Google Sheet** named "Daily Work Log"
2. **Enable APIs** in Google Cloud Console:
   - Google Sheets API
   - Google Drive API
3. **Create Service Account** and download credentials
4. **Share the sheet** with your service account email

### Environment Variables

Create `.streamlit/secrets.toml` with your Google credentials:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

## 🎨 Customization

### Styling

Edit `style.css` to customize the appearance:

```css
/* Customize colors, fonts, and layout */
h1 {
    color: #your-color;
    font-size: 2.5rem;
}
```

### Google Sheet Name

Change the sheet name in `main.py`:

```python
GOOGLE_SHEET_NAME = "Your Custom Sheet Name"
```

## 🔒 Security

- **Never commit** your `secrets.toml` file to version control
- **Use environment variables** for production deployments
- **Rotate service account keys** regularly
- **Limit service account permissions** to only what's needed

## 🐛 Troubleshooting

### Common Issues

1. **"No access token in response"**
   - Check that APIs are enabled
   - Verify service account has access to the sheet
   - Ensure OAuth scopes are correct

2. **"Spreadsheet not found"**
   - Verify sheet name matches exactly
   - Check that sheet is shared with service account

3. **"Permission denied"**
   - Ensure service account has Editor permissions
   - Check that the sheet exists and is accessible

### Getting Help

- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Review [Google Sheets API documentation](https://developers.google.com/sheets/api)
- Open an issue on GitHub for bugs or feature requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Google Sheets integration via [gspread](https://github.com/burnash/gspread)
- Styled with custom CSS

---

**Happy logging! 📝✨**



=======
📊 Daily Work Logger

A polished Streamlit web application for logging daily work activities directly to Google Sheets. Track your projects, accomplishments, and insights with an intuitive interface.

✨ Features

🎨 Beautiful UI with custom CSS styling

📊 Google Sheets Integration - automatically saves to your spreadsheet

💅 Automated Sheet Formatting - auto-sizes columns and styles the header row

📝 Flexible Input - supports multi-column formats

🖱️ Click-to-Run - Includes .bat (Windows) and .sh (Mac/Linux) scripts to launch the app instantly

🚀 Quick Start

Prerequisites

Python 3.8 or higher

A Google Cloud Project with:

Google Sheets API enabled

Google Drive API enabled

A Google Service Account with Editor access to your target Google Sheet.

Installation

Clone the repository (or download all the files):
Put app.py, style.css, requirements.txt, run_logger.bat, and run_logger.sh in the same folder.

Install dependencies:
Open your terminal or command prompt in that folder and run:

pip install -r requirements.txt


Set up Google Sheets credentials:

Go to your Google Cloud Project and create a Service Account.

Create a JSON key for the service account and download it.

Create a new folder named .streamlit in your project directory.

Inside .streamlit, create a file named secrets.toml (i.e., .streamlit/secrets.toml).

Open the downloaded JSON key (it's a text file) and copy its entire contents.

Paste the contents into secrets.toml and put [gcp_service_account] right at the top, above the text you just pasted.

Example .streamlit/secrets.toml:

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project-id.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "[https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com](https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com)"


Share your Google Sheet:

Create a new Google Sheet. You can name it "Daily Work Log" or anything else.

In app.py, make sure the GOOGLE_SHEET_NAME variable matches your sheet's name exactly.

Click the "Share" button on your Google Sheet.

Paste the client_email from your secrets.toml file into the sharing box.

Make sure to give it "Editor" permissions and click "Send".

Run the application:

On Windows: Just double-click run_logger.bat.

On Mac/Linux: You may need to run this command in your terminal one time to make the script executable: chmod +x run_logger.sh. After that, you can just double-click run_logger.sh.

📋 Usage

Input Format

The app accepts CSV data in two formats.

3 Columns (Date will be added automatically):

Project / Category,Accomplishment,Key Insight / Outcome


4 Columns (Date included):

Date,Project / Category,Accomplishment,Key Insight / Outcome


Example Data

8/12/2025,AutoGen,Practiced prompt workflows and configuration,Understood prompt orchestration and API flow

🐛 Troubleshooting

Error: No access token in response.

This is almost always a system clock issue. Make sure your computer's date and time are set to "Set time automatically".

If your clock is correct, try generating a new JSON key for your service account and updating your secrets.toml file.

Error: SpreadsheetNotFound

Check that the GOOGLE_SHEET_NAME variable in app.py exactly matches the name of your Google Sheet.

Make sure you have shared the sheet with your service account's client_email.

Error: PermissionError or insufficient permissions

Go to your Google Sheet's "Share" settings and make sure your service account has the "Editor" role, not "Viewer" or "Commenter".

Make sure you have enabled both the Google Sheets API and the Google Drive API in your Google Cloud project.

📄 License

This project is licensed under the MIT License.
