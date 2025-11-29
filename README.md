AI Agent: Smart Resume Screener 🤖📄

1. Overview

This AI Agent automates the initial screening process for recruitment. By leveraging Large Language Models (LLMs), it analyzes PDF resumes against a specific Job Description (JD) to provide a semantic match score, identifying strengths and missing skills instantly.

Category: People & HR (Resume Screening Agent)

2. Features

Semantic Matching: Goes beyond keyword matching to understand context.

Automated Parsing: Extracts text from PDF resumes automatically.

Scoring & Ranking: Provides a 0-100 match score for every candidate.

Detailed Analysis: Lists specific "Key Strengths" and "Missing Skills" for every profile.

Exportable Data: Allows HR to download the ranking matrix as a CSV.

3. Tech Stack

Language: Python

Frontend: Streamlit

AI Model: Google Gemini 1.5 Flash (via google-generativeai)

PDF Processing: PyPDF2

Data Handling: Pandas

4. Setup & Run Instructions

Prerequisites

Python 3.8 or higher

A Google Gemini API Key

Installation

Clone the repository:

git clone <your-repo-link>
cd resume-screener


Install dependencies:

pip install -r requirements.txt


Run the agent:

streamlit run app.py


Usage:

Enter your API Key in the sidebar.

Paste a Job Description.

Upload PDF resumes.

Click "Analyze Candidates".

5. Architecture Logic

Input Layer: Takes unstructured data (PDFs) and structured intent (JD text).

Processing Layer: PyPDF2 extracts raw text.

Cognitive Layer: The text is wrapped in a "Persona Prompt" (acting as an HR Manager) and sent to the LLM.

Structured Output: The LLM is forced to return valid JSON.

Presentation Layer: Data is parsed into a Pandas DataFrame and rendered in Streamlit.

6. Potential Improvements

Batch Processing: Using asynchronous calls for analyzing 100+ resumes faster.

RAG Integration: Connecting to a vector database to search a history of past candidates.

Email Integration: Auto-sending rejection/interview emails based on score.