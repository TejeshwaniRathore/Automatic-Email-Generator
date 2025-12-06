# automatic-email-generator
# 📨 AI-Powered Automatic Email Generator

This project is an intelligent email assistant that automatically fetches important, personal emails from your Gmail account, uses a Large Language Model (LLM) to generate contextual replies, and provides a simple web interface to review, edit, and send them.

It's designed to streamline your inbox management by filtering out noise and drafting thoughtful responses based on the entire conversation history.

![Demo GIF](https://path-to-your-demo-image.gif) <!-- It's highly recommended to add a screenshot or GIF of the app in action! -->

## ✨ Features

- **Smart Email Fetching**: Connects to your Gmail account to fetch unread emails marked as `IMPORTANT`.
- **Automated Filtering**: Intelligently ignores automated emails (like newsletters and security alerts) to focus on personal conversations.
- **Context-Aware AI Replies**: Analyzes the full email thread to generate relevant and coherent draft replies.
- **Flexible LLM Support**: Seamlessly integrates with OpenAI, Groq, or a local Ollama instance, with a built-in fallback system.
- **Interactive UI**: A user-friendly web interface built with Streamlit to view emails, generate replies, and send them with a single click.
- **Secure Authentication**: Uses Google's OAuth 2.0 for secure API access and keeps all credentials safe using environment variables.

## 🛠️ Tech Stack & Architecture

- **Backend**: **FastAPI** for a high-performance, robust API.
- **Frontend**: **Streamlit** for a simple, interactive Python-based web interface.
- **Email Service**: **Gmail API** for all email operations.
- **LLM Services**: **OpenAI**, **Groq**, and **Ollama** for AI-powered text generation.
- **Authentication**: **Google OAuth 2.0** for secure, token-based access to Gmail.

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### Prerequisites

- Python 3.9+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AUTOMATIC_EMAIL_GENERATOR.git
cd AUTOMATIC_EMAIL_GENERATOR
```

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
*(Note: You will need to create a `requirements.txt` file. See the section below.)*

### 4. Configure Environment Variables

This project uses a `.env` file to manage secret keys.

1.  **Create the `.env` file** by copying the example template:
    ```bash
    cp .env.example .env
    ```

2.  **Add LLM API Keys**: Open the `.env` file and add your API key for at least one of the supported services (OpenAI or Groq). The system will prioritize them in that order.
    ```.env
    OPENAI_API_KEY="sk-..."
    GROQ_API_KEY="gsk_..."
    ```

3.  **Add Gmail API Credentials**:
    - Go to the Google Cloud Console.
    - Create a new project and enable the **Gmail API**.
    - Create an **OAuth 2.0 Client ID** for a **Desktop app**.
    - Copy the `Client ID` and `Client Secret` into your `.env` file.
    ```.env
    GMAIL_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
    GMAIL_CLIENT_SECRET="your-google-client-secret"
    ```

### 5. Generate Your Gmail Refresh Token

Run the provided script to authorize the application and generate a refresh token. This is a one-time setup step.

```bash
python build_gmail_service.py
```

This will open a browser window asking you to log in and grant permission. After you approve, a **refresh token** will be printed in your terminal. Copy this token and paste it into your `.env` file.

```.env
GMAIL_REFRESH_TOKEN="1//04..."
```

### 6. Run the Application

You need to run the backend and frontend servers in two separate terminals.

**Terminal 1: Start the Backend (FastAPI)**
```bash
uvicorn app.main:app --reload
```
The backend will be available at `http://127.0.0.1:8000`.

**Terminal 2: Start the Frontend (Streamlit)**
```bash
streamlit run ui/streamlit_app.py
```
The web interface will open automatically in your browser at `http://localhost:8501`.

## 📖 How to Use

1.  Open the web application in your browser.
2.  Click **"Fetch Personal Emails"** to load unread, important messages.
3.  Select an email from the dropdown menu to view its content.
4.  Click **"Generate AI Reply"** to have the LLM draft a response.
5.  Review and edit the generated subject and body as needed.
6.  Click **"Send Reply"** to send the email.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.


