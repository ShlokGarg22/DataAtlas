# DataAtlas

DataScout Pro - Advanced Dataset Hub for discovering AI datasets across multiple sources with AI-powered recommendations.

## ✨ New Features

- 🤖 **Groq AI Integration**: Uses Groq's LLaMA 3.3 70B model to provide intelligent dataset recommendations
- 🎯 **Targeted Results**: AI generates specific, relevant dataset suggestions instead of generic searches
- 🔗 **Better Links**: More focused search queries that lead directly to actual datasets
- 💡 **Smart Insights**: Each recommendation includes AI-generated explanations of why it's relevant

## Setup Instructions

### 1. Create and Activate Virtual Environment

**Windows:**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root and add your Groq API key:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
GROQ_API_KEY=your_actual_groq_api_key_here
```

Get your Groq API key from: <https://console.groq.com/keys>

### 4. Run the Application

```bash
streamlit run main.py
```

## Features

- 🔍 Search across multiple data sources:
  - Hugging Face Hub
  - Wikipedia
  - YouTube (transcripts)
  - Reddit
  - Stack Overflow
  - Kaggle

- 🎯 Advanced filtering:
  - Data type (Conversational, Factual, Instructional, Q&A, Code, Multimedia)
  - Format (JSONL, CSV, Markdown, Raw Text, Audio, Parquet)
  - Cost (Free, Paid, All)

- 📊 Organized results by source with metadata

## Data Sources

Each source module in the `sources/` directory provides search functionality:

- `hf_service.py` - Hugging Face datasets
- `wiki_service.py` - Wikipedia articles
- `yt_service.py` - YouTube video transcripts
- `reddit_service.py` - Reddit discussions
- `stack_overflow_service.py` - Stack Overflow Q&A
- `kaggle_service.py` - Kaggle datasets and competitions

