# 📝 Daily AI Work Logger

A beautiful **Streamlit** web application powered by the **Gemini AI API**, designed to help you log your daily work activities directly into **Google Sheets**.
Track your projects, accomplishments, insights, and blockers simply by writing a natural-language summary of your day.

---

## ✨ Features

* 🧠 **Natural Language Input:**
  No need to format CSVs — just describe your day (e.g., *“Today I finished the homepage for the X project.”*).

* 🤖 **AI-Powered Parsing:**
  Uses Gemini AI to intelligently extract and categorize your work into structured columns.

* 🎨 **Beautiful UI:**
  Clean and minimal interface with custom CSS styling.

* 📊 **Google Sheets Integration:**
  Automatically appends your parsed work logs as new rows in a Google Sheet.

* 🔄 **Real-time Updates:**
  Instantly preview parsed data before saving.

* 🔐 **Secure Secrets Handling:**
  All API keys and credentials are safely managed via Streamlit Secrets.

---

## 🚀 Quick Start

### 🧩 Prerequisites

* Python **3.8+**
* Google Cloud Project with **Sheets API** and **Drive API** enabled
* A **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)
* A **Google Service Account** with proper permissions

---

### ⚙️ Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Vivek5143/Daily-Work-Logger.git
cd Daily-Work-Logger
```

#### 2. Create and Activate Virtual Environment

**Windows (CMD):**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

### Create `.streamlit/secrets.toml`

Create a folder named `.streamlit` in your project directory.
Inside it, create a file called `secrets.toml` and paste the following template:

```toml
### Gemini API Key (from Google AI Studio)
gemini_api_key = "...your...gemini...api...key"

### Google Cloud Service Account credentials
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = """-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_GOES_HERE
-----END PRIVATE KEY-----"""
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

---

## 📄 Google Sheet Setup

1. Create a **Google Sheet** (e.g., `Daily Work Log`).
2. Share it with your **Service Account email** (from the credentials above).
3. Grant **Editor permissions**.

---

## ▶️ Run the Application

Rename your main app file to `main.py` (or adjust the command) and run:

```bash
streamlit run main.py
```

---

## 💼 Usage

### 1. Write Your Summary

Type a few sentences about what you worked on today.
Example:

> “Worked on the login page and fixed the timeout bug.”

### 2. Click **“Parse Work Log”**

Gemini AI will automatically detect and extract:

* **Date**
* **Project / Category**
* **Accomplishment**
* **Key Insight / Blocker**

### 3. Preview Your Parsed Data

Review what the AI extracted.

### 4. Click **“Save to Google Sheet”**

Your structured log will be added to your Google Sheet.

---

## 💡 Example

**Input:**

```text
Today was all about the new user dashboard. I finished the main layout with the new charting library. I also had a meeting about the Q4 roadmap, which helped clarify our goals. The only blocker is that I'm still waiting on the final API endpoints from the backend team.
```

**AI-Parsed Output:**

| Date       | Project / Category | Accomplishment                                 | Key Insight / Blocker                                |
| ---------- | ------------------ | ---------------------------------------------- | ---------------------------------------------------- |
| 2025-10-29 | User Dashboard     | Finished main layout with new charting library | —                                                    |
| 2025-10-29 | Q4 Roadmap         | Meeting clarified goals                        | —                                                    |
| 2025-10-29 | Backend API        | —                                              | Waiting on final API endpoints from the backend team |

---

## 🎨 Customization

### Styling

Edit `style.css` to change fonts, colors, and UI layout.

### Sheet Name

In your Python file, update:

```python
GOOGLE_SHEET_NAME = "Your Custom Sheet Name"
```

---

## 🔒 Security

* Never commit `.streamlit/secrets.toml` to GitHub.
* Add `.streamlit/secrets.toml` to your `.gitignore`.
* Restrict your service account permissions (Sheets + Drive only).

---

## 🐛 Troubleshooting

| Issue                                     | Possible Fix                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------------ |
| **Gemini API Error / Key not found**      | Check `gemini_api_key` in `secrets.toml` and restart Streamlit.                |
| **Spreadsheet not found**                 | Ensure the sheet name matches exactly and is shared with your service account. |
| **Permission denied / Incorrect padding** | Check private key formatting (use triple quotes `"""` as shown).               |
| **AI not parsing correctly**              | Try simplifying your input text or ensure the Gemini key is valid.             |

---

## 🤝 Contributing

1. **Fork** the repository
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature
   ```
3. **Commit** your changes and **push**:

   ```bash
   git push origin feature/your-feature
   ```
4. Submit a **Pull Request** 🎉

---

## 📄 License

This project is licensed under the **MIT License**.

---

## Acknowledgments

Built with ❤️ using:

* **Streamlit**
* **Google Gemini API**
* **gspread**
