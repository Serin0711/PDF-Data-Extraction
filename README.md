# PDF-Data-Extraction

# Tamil PDF Data Extraction

This Python script extracts data from Tamil PDFs containing voter information. It utilizes OCR (Optical Character Recognition) techniques to extract text from images generated from the PDF pages.

## Prerequisites

Ensure you have the following libraries installed:

- OpenCV (`cv2`)
- EasyOCR (`easyocr`)
- pandas (`pandas`)
- PyTesseract (`pytesseract`)
- pdf2image (`pdf2image`)
- PIL (`Pillow`)

You can install these libraries using `pip`:

```bash
pip install opencv-python-headless easyocr pandas pytesseract pdf2image Pillow
```

You also need to have Tesseract OCR installed on your system and set up properly. Make sure to set the TESSDATA_PREFIX environment variable to point to the location of Tesseract's language data files. For example:

```bash
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
```

## Usage

1. Place your PDF file (`tamil.pdf`) in the same directory as the script.
2. Run the script `blur.py`.

```bash
python blur.py
```

The script will perform the following steps:

- Convert the PDF pages to images.
- Crop and save specific regions of interest from the images.
- Extract text from the cropped images using OCR.
- Save the extracted text data to Excel (`tamil_excel_data.xlsx`).

## Configuration

You can adjust the coordinates and other parameters in the script according to your specific PDF layout and requirements. Update the `coordinates_dict`, `coordinates`, and other variables as needed.
