# Install required libraries(run in the terminal)
#pip install PyPDF2 pdfplumber spacy transformers gdown

# Download spaCy model(run in the terminal)
#python -m spacy download en_core_web_sm

# Import necessary libraries

import re
import spacy

# Import necessary libraries
import gdown
import pdfplumber
from transformers import pipeline

# Download file from Google Drive
def download_file_from_drive(drive_url, output_path):
    """
    Downloads a file from a Google Drive link.
    """
    gdown.download(drive_url, output_path, quiet=False)

# Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from all pages of a PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Summarize large text
def summarize_large_text(text, chunk_size=1024, max_summary_length=200):
    """
    Summarizes large text by splitting it into chunks, summarizing each chunk, 
    and combining the results.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summaries = []

    # Split text into chunks
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        try:
            summary = summarizer(chunk, max_length=max_summary_length, min_length=50, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            summaries.append(f"Error summarizing chunk: {e}")
    
    # Combine all summaries into a single text
    return " ".join(summaries)

# Main function to summarize a PDF from Google Drive
def summarize_pdf_from_drive(drive_url):
    """
    Downloads a PDF from Google Drive, extracts its text, and generates a summary.
    """
    local_pdf_path = "downloaded_file.pdf"  # Temporary local file path
    download_file_from_drive(drive_url, local_pdf_path)  # Download the PDF
    
    # Extract text from the PDF
    text = extract_text_from_pdf(local_pdf_path)
    if not text.strip():
        return "The PDF does not contain readable text."

    # Summarize the extracted text
    summary = summarize_large_text(text)
    return summary

if __name__ == "__main__":
    # Provide your Google Drive link here
    google_drive_link = "https://drive.google.com/uc?export=download&id=1jguXFqGgYkbeF5X9jFJ4ts50m-VJ1rCu"
    
    # Generate and print the summary
    print("Downloading and summarizing the PDF...")
    pdf_summary = summarize_pdf_from_drive(google_drive_link)
    print("\nSummary of the PDF:\n")
    print(pdf_summary)
