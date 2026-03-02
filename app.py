import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_bytes

st.title("PDF to Excel using OCR")

pdf_file = st.file_uploader("Upload PDF", type="pdf")

def ocr_pdf(pdf_file):
    pages = convert_from_bytes(pdf_file.read(), dpi=300)
    rows = []

    for page_no, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page)
        for line_no, line in enumerate(text.split("\n"), start=1):
            if line.strip():
                rows.append([page_no, line_no, line])

    return pd.DataFrame(rows, columns=["Page", "Line", "Text"])

if pdf_file:
    if st.button("Convert"):
        df = ocr_pdf(pdf_file)

        st.success("OCR Completed")
        st.dataframe(df)

        df.to_excel("output.xlsx", index=False)
        st.download_button(
            "Download Excel",
            data=open("output.xlsx", "rb"),
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
