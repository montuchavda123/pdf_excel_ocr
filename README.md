# 📄 PDF to Excel OCR App (Streamlit)

This project is a **Streamlit-based OCR application** that converts PDF files into structured Excel output using Optical Character Recognition (OCR).

---

## 🚀 Features
- Upload single or multiple PDF files
- Convert scanned PDFs to text using Tesseract OCR
- Display extracted data in tabular format
- Download results as an Excel file
- Built with Streamlit for quick UI deployment

---

## 🛠 Tech Stack
- Python
- Streamlit
- Tesseract OCR
- Poppler
- Pandas
- pdf2image

---

## 📦 Required Dependencies

### Python Packages (requirements.txt)
- streamlit
- pandas
- pytesseract
- pdf2image
- Pillow
- openpyxl

### System Packages (packages.txt)
- tesseract-ocr
- poppler-utils

---

## 🌍 Deployment

This application is deployed using **Hugging Face Spaces** because:
- OCR requires system-level dependencies
- Streamlit Cloud does not support installing Tesseract & Poppler

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt