import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_bytes

st.title("PDF to Excel using OCR (Multiple Files)")

pdf_files = st.file_uploader(
    "Upload PDF files (max 15)",
    type="pdf",
    accept_multiple_files=True
)

def ocr_pdf(pdf_file):
    pages = convert_from_bytes(pdf_file.read(), dpi=300)
    rows = []

    for page_no, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page)
        for line_no, line in enumerate(text.split("\n"), start=1):
            if line.strip():
                rows.append([page_no, line_no, line])

    return pd.DataFrame(rows, columns=["Page", "Line", "Text"])

if pdf_files and len(pdf_files) <= 15:
    if st.button("Convert to Excel"):
        output_file = "ocr_output.xlsx"

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            for pdf in pdf_files:
                df = ocr_pdf(pdf)
                sheet_name = pdf.name[:31]  # Excel sheet name limit
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        st.success("OCR completed for all PDFs")

        st.download_button(
            "Download Excel",
            data=open(output_file, "rb"),
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

elif pdf_files and len(pdf_files) > 15:
    st.warning("Please upload a maximum of 15 PDF files.")
