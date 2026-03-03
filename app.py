import streamlit as st
import pdfplumber
import pandas as pd

st.title("PDF Table to Excel (Exact Columns)")

pdf_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

def extract_table(pdf_file):
    all_tables = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

    return pd.concat(all_tables, ignore_index=True)

if pdf_files and st.button("Convert to Excel"):
    output_file = "table_output.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for pdf in pdf_files:
            df = extract_table(pdf)
            sheet_name = pdf.name[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    st.success("Table extracted successfully!")
    st.download_button(
        "Download Excel",
        data=open(output_file, "rb"),
        file_name=output_file
    )
