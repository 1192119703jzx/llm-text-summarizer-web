# LLM-Based Text Summarizer

This project is a Streamlit-based web application for text summarization. Users can input text or upload files to generate concise summaries using advanced language models. The app also allows users to manage their preferences, view summarization history, and customize the summarization style.

## Features

- **User Authentication**: Log in or sign up to save your preferences and history.
- **Text Summarization**: Summarize text in different styles (Formal, Casual, Technical).
- **Preference Management**: Create, edit, and delete summarization preferences.
- **History Management**: View and manage your summarization history.
- **Search Functionality**: Search through your summarization history by keywords.

## Requirements

- Python 3.10 or higher
- MongoDB (local or remote instance)
- Streamlit

## Usage
* Users can directly visit our app site: [llm-text-summarizer-app](https://llm-text-summarizer-web-production.up.railway.app)
* For users who want to develop and deploy by themselves, follow the instructions below.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm-text-summarizer-web
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     DB_URI=<your-mongodb-uri>
     DEEPSEEK_API=<your-deepseek-api-key>
     ```

4. Set up MongoDB:
   - **Option 1**: Use a cloud MongoDB instance (recommended):
     - Create a free MongoDB Atlas account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
     - Set up a new cluster and get your connection string
     - Use this connection string as your `DB_URI` in the `.env` file

   - **Option 2**: Install and run MongoDB locally on Linux:
     - **Ubuntu/Debian**:
       ```bash
       sudo apt update
       sudo apt install -y mongodb
       sudo systemctl start mongodb
       sudo systemctl enable mongodb
       ```
## Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run src/main.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## Deployment

This project is configured for deployment using [Railway](https://railway.app/). The `railway.json` file contains the necessary configuration.

## Folder Structure

- `src/`: Contains the main application code.
  - `database.py`: Handles database operations.
  - `db_instance.py`: Initializes the database instance.
  - `deepseek_api.py`: Integrates with the DeepSeek API for text summarization.
  - `user.py`, `home.py`, `preference.py`, `summarization.py`: Define the Streamlit pages.
  - `prompt/`: Contains predefined prompts for different summarization styles.
- `test.py`: Unit tests for the database module.
- `requirements.txt`: Python dependencies.
- `railway.json`: Configuration for Railway deployment.

## Managing MongoDB

### Stopping MongoDB on Linux
- **Ubuntu/Debian**:
  ```bash
  sudo systemctl stop mongodb
  ```

### Checking MongoDB Status on Linux
- **Ubuntu/Debian/RHEL/CentOS/Fedora**:
  ```bash
  sudo systemctl status mongodb    
  ```
