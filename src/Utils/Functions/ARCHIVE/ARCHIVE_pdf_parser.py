from llmsherpa.readers import LayoutPDFReader

def parse_pdf(pdf_path):
    # Configure API endpoint
    api_url = "http://localhost:8080/api/parseDocument?renderFormat=all"
    
    # Initialize reader
    pdf_reader = LayoutPDFReader(api_url)
    
    # Read file as binary
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    
    # Pass contents directly
    doc = pdf_reader.read_pdf("dummy_filename.pdf", contents=pdf_bytes)
    
    return doc

if __name__ == "__main__":
    # Use raw string for Windows path
    pdf_path = r"C:\Users\Anand\Documents\Code Projects\agent_data_platform\experiments\agent_pdf_pipeline\Uploads\samples\monolith_realtime_recommend.pdf"
    
    print("🚀 Starting PDF parsing process...")
    doc = parse_pdf(pdf_path)
    
    # If we get here, parsing succeeded
    print("\n✅ Successfully parsed PDF!")
    print(f"📑 First section title: {doc.sections()[0].title}")
    print(f"📊 Tables found: {len(doc.tables())}")