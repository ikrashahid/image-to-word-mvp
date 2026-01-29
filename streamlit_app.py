"""
MVP Streamlit Web Application - Elegant Edition
===============================================

A beautiful, user-friendly web interface for the Image-to-Word converter.

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
    page_title="Image to Word Converter",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for elegant styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        color: white;
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2em;
        font-weight: 300;
        margin-top: 0;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 2em;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-size: 1em;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.3rem;
    }
    
    .feature-desc {
        font-size: 0.85em;
        color: #718096;
        line-height: 1.5;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(to bottom right, #f7fafc, #edf2f7);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px dashed #cbd5e0;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #667eea;
        background: linear-gradient(to bottom right, #f7fafc, #e6f0ff);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1em;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }
    
    .stDownloadButton>button:hover {
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.6);
    }
    
    /* Image Preview */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin: 2rem 0;
    }
    
    /* Info Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Card Style Elements */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    
    /* Separator */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #cbd5e0, transparent);
        margin: 2rem 0;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: transparent;
    }
    
    .stFileUploader > div {
        border: none;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #f0fff4;
        border-left: 4px solid #48bb78;
        border-radius: 12px;
    }
    
    .stError {
        background-color: #fff5f5;
        border-left: 4px solid #f56565;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">✨ Image to Word</div>
    <div class="hero-subtitle">Transform your documents with AI-powered precision</div>
</div>
""", unsafe_allow_html=True)

# Feature Cards
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Format Perfect</div>
        <div class="feature-desc">Preserves bold, italic, and headings</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Lightning Fast</div>
        <div class="feature-desc">Results in seconds</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Powered</div>
        <div class="feature-desc">Google Gemini technology</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <div class="feature-title">Secure</div>
        <div class="feature-desc">No data stored</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Expandable sections with better styling
col1, col2 = st.columns(2)

with col1:
    with st.expander("📖 How It Works"):
        st.markdown("""
        **Simple 3-Step Process:**
        
        1. 📤 **Upload** your image
        2. ⚙️ **Convert** with AI
        3. 💾 **Download** your Word doc
        
        Works with scanned documents, photos, and screenshots!
        """)

with col2:
    with st.expander("💡 Pro Tips"):
        st.markdown("""
        **For Best Results:**
        
        ✓ Use clear, well-lit images  
        ✓ High resolution preferred  
        ✓ Avoid blur and glare  
        ✓ Single page works best  
        """)

st.markdown("<br>", unsafe_allow_html=True)

# Main upload section
uploaded_file = st.file_uploader(
    "Drop your image here or click to browse",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, PNG",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Display uploaded image in elegant container
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Image info in elegant card
    st.markdown(f"""
    <div class="info-card">
        <strong>📊 Image Details:</strong> {image.format} format • {image.size[0]} × {image.size[1]} px • {uploaded_file.name}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Convert button
    if st.button("🚀 Convert to Word Document", type="primary"):
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Save uploaded file
            status_text.markdown("**⏳ Preparing your image...**")
            progress_bar.progress(10)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                input_path = tmp_file.name
            
            time.sleep(0.3)
            
            # Step 2: Initialize converter
            status_text.markdown("**🔧 Initializing AI engine...**")
            progress_bar.progress(25)
            converter = GeminiImageToWordConverter()
            time.sleep(0.3)
            
            # Step 3: Process
            status_text.markdown("**🤖 Extracting text with AI...**")
            progress_bar.progress(50)
            
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
            
            # Run conversion
            result = converter.convert(input_path, output_path)
            
            progress_bar.progress(90)
            status_text.markdown("**✨ Finalizing document...**")
            time.sleep(0.3)
            
            # Cleanup input
            if os.path.exists(input_path):
                os.remove(input_path)
            
            # Step 4: Show results
            if result['success']:
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                # Success with balloons
                st.balloons()
                
                st.success("🎉 **Conversion Complete!** Your document is ready to download.")
                
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
                
                # Info tip
                st.info("💡 **Note:** All formatting, headings, and text alignment have been preserved in your Word document.")
                
                # Cleanup output
                if os.path.exists(output_path):
                    os.remove(output_path)
                
            else:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ **Conversion Failed:** {result['message']}")
                st.info("💡 **Tip:** Try uploading a clearer image or check your API configuration.")
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ **Error:** {str(e)}")
            st.info("💡 **Need Help?** Make sure your image is clear and properly formatted.")

else:
    # Elegant empty state
    st.markdown("""
    <div class="upload-section">
        <div style="font-size: 4em; margin-bottom: 1rem;">📄</div>
        <h3 style="color: #2d3748; margin-bottom: 0.5rem;">Ready to Convert?</h3>
        <p style="color: #718096; font-size: 1.1em;">Upload an image to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use cases in elegant grid
    st.markdown("<h3 style='text-align: center; color: #2d3748; margin-top: 2rem;'>Perfect For</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div style="font-size: 2.5em;">📋</div>
            <strong>Business Documents</strong>
            <p style="font-size: 0.9em; color: #718096; margin-top: 0.5rem;">
            Invoices, receipts, contracts, forms
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div style="font-size: 2.5em;">📚</div>
            <strong>Academic Papers</strong>
            <p style="font-size: 0.9em; color: #718096; margin-top: 0.5rem;">
            Research, reports, essays, notes
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <div style="font-size: 2.5em;">✍️</div>
            <strong>Handwritten</strong>
            <p style="font-size: 0.9em; color: #718096; margin-top: 0.5rem;">
            Notes, letters, manuscripts
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #a0aec0; font-size: 0.9em; padding: 2rem 0;'>
    <p style='margin: 0;'>🔐 Your privacy matters - images are processed securely and never stored</p>
    <p style='margin-top: 0.5rem;'>Made with ❤️ using AI technology</p>
</div>
""", unsafe_allow_html=True)
