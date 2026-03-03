import streamlit as st
import pdfplumber
import pandas as pd
import re

st.title("GRN PDF to Excel Converter")

pdf_files = st.file_uploader("Upload GRN PDF files", type="pdf", accept_multiple_files=True)

def extract_grn_data(pdf):
    data = {}
    
    with pdfplumber.open(pdf) as pdf_file:
        text = ""
        for page in pdf_file.pages:
            text += page.extract_text() + "\n"
    
    # Extract required fields using regex
    data["File Name"] = pdf.name
    
    data["GRN No"] = re.search(r"GRN No\s*:\s*(\S+)", text).group(1) if re.search(r"GRN No\s*:\s*(\S+)", text) else ""
    
    data["Receipt Date"] = re.search(r"Receipt Date\s*(\d{2}-\w{3}-\d{4})", text)
    data["Receipt Date"] = data["Receipt Date"].group(1) if data["Receipt Date"] else ""
    
    data["Farmer Name"] = re.search(r"Farmer Name\s*(.*?)\s*PO Code", text)
    data["Farmer Name"] = data["Farmer Name"].group(1).strip() if data["Farmer Name"] else ""
    
    data["Contact No"] = re.search(r"Contact No\s*(\d+)", text)
    data["Contact No"] = data["Contact No"].group(1) if data["Contact No"] else ""
    
    data["Address"] = re.search(r"Address\s*(.*?)\s*Bank Name", text)
    data["Address"] = data["Address"].group(1).strip() if data["Address"] else ""
    
    data["Bank Name & Branch"] = re.search(r"Bank Name & Branch\s*(.*?)\s*IFSC Code", text)
    data["Bank Name & Branch"] = data["Bank Name & Branch"].group(1).strip() if data["Bank Name & Branch"] else ""
    
    data["IFSC Code"] = re.search(r"IFSC Code:\s*(\S+)", text)
    data["IFSC Code"] = data["IFSC Code"].group(1) if data["IFSC Code"] else ""
    
    data["Account Number"] = re.search(r"Account Number\s*(\d+)", text)
    data["Account Number"] = data["Account Number"].group(1) if data["Account Number"] else ""
    
    # ---------------- WEIGHTMENT DETAILS ----------------
    data["Gross Wt (Kgs)"] = re.search(r"Gross Wt\(Kgs\)\s*(\d+)", text)
    data["Gross Wt (Kgs)"] = data["Gross Wt (Kgs)"].group(1) if data["Gross Wt (Kgs)"] else ""
    
    data["Nett Weight (Kgs)"] = re.search(r"Nett Weights\(Kgs\)\s*(\d+)", text)
    data["Nett Weight (Kgs)"] = data["Nett Weight (Kgs)"].group(1) if data["Nett Weight (Kgs)"] else ""
    
    data["Pay Weight (Kgs)"] = re.search(r"Pay Weights\(Kgs\)\s*(\d+)", text)
    data["Pay Weight (Kgs)"] = data["Pay Weight (Kgs)"].group(1) if data["Pay Weight (Kgs)"] else ""
    
    data["Bags Count"] = re.search(r"Bags Count\s*(\d+)", text)
    data["Bags Count"] = data["Bags Count"].group(1) if data["Bags Count"] else ""
    
    
    # ---------------- QUALITY DETAILS ----------------
    data["Matti %"] = re.search(r"Matti\s*\.?(\d+\.?\d*)", text)
    data["Matti %"] = data["Matti %"].group(1) if data["Matti %"] else ""
    
    data["Damaged %"] = re.search(r"Damaged\s*(\d+\.?\d*)", text)
    data["Damaged %"] = data["Damaged %"].group(1) if data["Damaged %"] else ""
    
    data["Fotri %"] = re.search(r"Fotri\s*(\d+\.?\d*)", text)
    data["Fotri %"] = data["Fotri %"].group(1) if data["Fotri %"] else ""
    
    data["Moisture %"] = re.search(r"Moisture\s*(\d+\.?\d*)", text)
    data["Moisture %"] = data["Moisture %"].group(1) if data["Moisture %"] else ""
    
    data["Dabba Weight"] = re.search(r"Dabba Weight\s*(\d+)", text)
    data["Dabba Weight"] = data["Dabba Weight"].group(1) if data["Dabba Weight"] else ""
    
    data["Total Value"] = re.search(r"Total Value\s*([\d,\.]+)", text)
    data["Total Value"] = data["Total Value"].group(1) if data["Total Value"] else ""
    
    return data


if pdf_files and st.button("Convert to Excel"):
    
    all_data = []
    
    for pdf in pdf_files:
        extracted = extract_grn_data(pdf)
        all_data.append(extracted)
    
    df = pd.DataFrame(all_data)
    
    output_file = "GRN_Output.xlsx"
    df.to_excel(output_file, index=False)
    
    st.success("GRN PDFs converted successfully!")
    st.dataframe(df)
    
    with open(output_file, "rb") as f:
        st.download_button("Download Excel", f, file_name=output_file)

