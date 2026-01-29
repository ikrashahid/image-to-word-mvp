# Image to Word Converter

A Python application that converts scanned documents and images into formatted Word documents while preserving text formatting like bold, italic, headings, and alignment.

## What It Does

Takes an image of a document and creates a Word file that maintains the original formatting including:
- Bold and italic text
- Headings (H1, H2, H3)
- Text alignment (left, center, right)
- Paragraph structure

## Requirements

- Python 3.8+
- Google Gemini API key

### Python Packages

```bash
pip install opencv-python pillow streamlit python-docx requests numpy
```

## Setup

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set your API key as an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or edit line 49 in `mvp_converter.py` to add your key directly.

## Running the Application

### Web Interface (Recommended)

```bash
streamlit run streamlit_app.py
```

Open your browser to the URL shown (usually http://localhost:8501)

### Command Line

```python
from mvp_converter import convert_image_to_word

result = convert_image_to_word('input.jpg', 'output.docx')
print(result['message'])
```

## How to Use

1. Upload an image (JPG or PNG)
2. Click the convert button
3. Download your formatted Word document

## Tips for Best Results

- Use clear, high-resolution images
- Ensure good lighting and minimal blur
- Single-page documents work best
- Avoid glare or shadows on the document

## How It Works

The conversion process has four steps:

1. **Image Preprocessing** - Enhances image quality using OpenCV (grayscale conversion, denoising, contrast enhancement)
2. **Text Extraction** - Uses Google Gemini AI to read the text and detect formatting
3. **Format Parsing** - Converts Gemini's output into structured data with formatting markers
4. **Document Generation** - Creates a Word document with python-docx, applying all detected formatting

## File Structure

- `mvp_converter.py` - Core conversion logic
- `streamlit_app.py` - Web interface
- `README.md` - This file

## Troubleshooting

**"API Error" message**
- Check your API key is correct
- Verify your API key has Gemini API access enabled

**Poor text recognition**
- Try uploading a clearer image
- Ensure the document has good contrast
- Avoid images with complex backgrounds

**Missing formatting**
- The AI does its best to detect formatting, but some styling may not be captured perfectly
- Manual review of the output is recommended for critical documents

## Privacy

Images are processed through the Gemini API but are not stored permanently. Temporary files are deleted after conversion.

## License

This project uses the Gemini API which has its own terms of service. Check Google's documentation for commercial use restrictions.

## Known Limitations

- Works best with printed text (handwriting recognition is less accurate)
- Complex layouts with multiple columns may not convert perfectly
- Tables and images are not currently supported
- Only processes one page at a time

## Future Improvements

Possible enhancements:
- Multi-page PDF support
- Table detection and conversion
- Image extraction and embedding
- Better handling of complex layouts
- Support for more formatting options (font colors, sizes, etc.)
