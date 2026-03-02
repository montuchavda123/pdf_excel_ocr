import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_bytes

# Required paths (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\Library\bin"

st.title("PDF to Excel using OCR")

pdf_file = st.file_uploader("Upload PDF", type="pdf")

if pdf_file:
    if st.button("Convert"):
        pages = convert_from_bytes(
            pdf_file.read(),
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        rows = []
        for page_no, page in enumerate(pages, start=1):
            text = pytesseract.image_to_string(page)
            for line_no, line in enumerate(text.split("\n"), start=1):
                if line.strip():
                    rows.append([page_no, line_no, line])

        df = pd.DataFrame(rows, columns=["Page", "Line", "Text"])

        st.success("OCR Completed")
        st.dataframe(df)

        df.to_excel("output.xlsx", index=False)
        st.download_button(
            "Download Excel",
            open("output.xlsx", "rb"),
            file_name="output.xlsx"

        )
