"""
MVP Streamlit Web Application
==============================

A user-friendly web interface for the Image-to-Word converter.

Features:
- Upload image (JPG/PNG)
- Real-time conversion
- Download formatted Word document
- Preview of extracted text
- Progress indicators
"""

import streamlit as st
import os
import tempfile
from mvp_converter import GeminiImageToWordConverter
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="Image to Word Converter - MVP",
    page_icon="📄",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .sub-header {
        text-align: center;
        color: #555;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1em;
        border-radius: 10px;
        margin: 1em 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.2em;
        padding: 0.5em;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📄 Image to Word Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Convert scanned documents to formatted Word files with AI</div>', unsafe_allow_html=True)

# Features section
with st.expander("✨ Key Features"):
    st.markdown("""
    - **🎯 Format Preservation**: Maintains bold, italic, headings, and alignment
    - **🤖 AI-Powered**: Uses Google Gemini for accurate OCR
    - **📝 Smart Detection**: Automatically identifies document structure
    - **⚡ Fast Processing**: Get results in seconds
    - **💾 Easy Download**: Get your formatted .docx file instantly
    """)

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Upload** your image (JPG or PNG format)
    2. Click **"Convert to Word Document"**
    3. Wait for processing (usually 5-15 seconds)
    4. **Download** your formatted Word document
    
    **Best Practices:**
    - Use clear, high-resolution images
    - Ensure good lighting and contrast
    - Avoid blurry or tilted images
    - Single-page documents work best
    """)

# Main upload section
st.markdown("---")
st.subheader("📤 Upload Your Image")

uploaded_file = st.file_uploader(
    "Choose an image file (JPG, PNG)",
    type=["jpg", "jpeg", "png"],
    help="Upload a scanned document or image with text"
)

if uploaded_file is not None:
    # Display uploaded image
    st.markdown("### 🖼️ Uploaded Image Preview")
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)  # Changed for older Streamlit compatibility
    
    # Image info
    st.info(f"📊 **Image Info:** {image.format} | Size: {image.size[0]}x{image.size[1]} pixels | File: {uploaded_file.name}")
    
    # Convert button
    st.markdown("---")
    
    if st.button("🚀 Convert to Word Document", type="primary"):
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Save uploaded file
            status_text.text("⏳ Preparing image...")
            progress_bar.progress(10)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                input_path = tmp_file.name
            
            time.sleep(0.5)  # Small delay for UX
            
            # Step 2: Initialize converter
            status_text.text("🔧 Preprocessing image...")
            progress_bar.progress(25)
            converter = GeminiImageToWordConverter()
            time.sleep(0.5)
            
            # Step 3: Process
            status_text.text(" Extracting text ")
            progress_bar.progress(50)
            
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
            
            # Run conversion
            result = converter.convert(input_path, output_path)
            
            progress_bar.progress(90)
            
            # Cleanup input
            if os.path.exists(input_path):
                os.remove(input_path)
            
            # Step 4: Show results
            if result['success']:
                progress_bar.progress(100)
                status_text.text("✅ Conversion completed!")
                time.sleep(0.5)
                
                # Success message
                st.success("🎉 **Conversion Successful!**")
                
                # Download button
                with open(output_path, 'rb') as f:
                    docx_data = f.read()
                
                st.download_button(
                    label="📥 Download Word Document",
                    data=docx_data,
                    file_name=f"converted_{uploaded_file.name.rsplit('.', 1)[0]}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
                
                # Info about the document
                st.info("💡 **Tip:** The document preserves formatting like bold, italic, headings, and alignment from your original image.")
                
                # Cleanup output
                if os.path.exists(output_path):
                    os.remove(output_path)
                
                # Show balloons
                st.balloons()
                
            else:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ **Conversion Failed:** {result['message']}")
                st.info("💡 Try uploading a clearer image or check your API key configuration.")
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ **Error:** {str(e)}")
            st.info("💡 Please try again or contact support if the issue persists.")

else:
    # Show example when no file uploaded
    st.markdown("---")
    st.info("👆 **Get Started:** Upload an image above to begin conversion")
    
    # Sample images showcase (optional)
    st.markdown("### 📸 Example Use Cases")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📋 Forms**
        - Invoices
        - Receipts
        - Applications
        """)
    
    with col2:
        st.markdown("""
        **📚 Documents**
        - Reports
        - Letters
        - Notes
        """)
    
    with col3:
        st.markdown("""
        **📝 Handwritten**
        - Notes
        - Manuscripts
        - Drafts
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9em;'>
    <p>🔐 Your images are processed securely and not stored</p>
    
</div>
""", unsafe_allow_html=True)