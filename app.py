import streamlit as st
import pdfplumber
import pandas as pd

st.title("PDF Table to Excel (Multiple PDFs → Multiple Sheets)")

pdf_files = st.file_uploader(
    "Upload up to 10 PDF files",
    type="pdf",
    accept_multiple_files=True
)

def extract_table(pdf_file):
    all_tables = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)

    return pd.DataFrame()  # SAFE fallback

if pdf_files:
    if len(pdf_files) > 10:
        st.warning("Please upload a maximum of 10 PDF files.")
    else:
        if st.button("Convert to Excel"):
            output_file = "pdf_tables_output.xlsx"
            sheet_written = False

            with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
                for pdf in pdf_files:
                    df = extract_table(pdf)
                    sheet_name = pdf.name.replace(".pdf", "")[:31]

                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        sheet_written = True

                # ✅ SAFETY SHEET (MANDATORY)
                if not sheet_written:
                    pd.DataFrame(
                        [["No tables detected in uploaded PDFs"]],
                        columns=["Message"]
                    ).to_excel(writer, sheet_name="Info", index=False)

            st.success("Excel file created successfully!")

            st.download_button(
                "Download Excel",
                data=open(output_file, "rb"),
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
