import streamlit as st
import pdfplumber, pandas as pd, pytesseract
from pdf2image import convert_from_bytes

st.title("PDF Table to Excel (Table + OCR)")

pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

def extract_table(pdf):
    # Try pdfplumber table first
    tables = []
    with pdfplumber.open(pdf) as p:
        for page in p.pages:
            for t in page.extract_tables():
                if t: tables.append(pd.DataFrame(t[1:], columns=t[0]))
    if tables: return pd.concat(tables, ignore_index=True)
    
    # OCR fallback
    pdf.seek(0)
    pages = convert_from_bytes(pdf.read(), dpi=300)
    rows = []
    for page in pages:
        for line in pytesseract.image_to_string(page).split('\n'):
            if line.strip(): rows.append(line.split())
    if rows: return pd.DataFrame(rows[1:], columns=rows[0])
    return pd.DataFrame()  # empty if nothing found

if pdf_files and st.button("Convert to Excel"):
    output_file = "table_output.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for pdf in pdf_files:
            df = extract_table(pdf)
            if not df.empty: df.to_excel(writer, sheet_name=pdf.name[:31], index=False)
        # safety sheet if all PDFs empty
        if all(extract_table(f).empty for f in pdf_files):
            pd.DataFrame([["No tables found"]], columns=["Info"]).to_excel(writer, sheet_name="Info", index=False)

    st.success("PDFs converted to Excel successfully!")
    st.download_button("Download Excel", data=open(output_file,"rb"), file_name=output_file)
