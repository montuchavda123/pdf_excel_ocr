import streamlit as st
import camelot
import pandas as pd

st.title("PDF Table to Excel (Exact Columns)")

pdf_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

if pdf_files and st.button("Convert to Excel"):
    output_file = "table_output.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for pdf in pdf_files:
            tables = camelot.read_pdf(
                pdf,
                pages="all",
                flavor="lattice"  # detects table borders
            )

            for i, table in enumerate(tables):
                df = table.df
                df.columns = df.iloc[0]  # first row as header
                df = df[1:]              # remove header row

                sheet_name = f"{pdf.name[:20]}_{i+1}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    st.success("Table extracted perfectly!")
    st.download_button(
        "Download Excel",
        data=open(output_file, "rb"),
        file_name=output_file
    )
