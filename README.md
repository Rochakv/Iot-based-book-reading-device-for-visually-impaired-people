# Iot-based-book-reading-device-for-visually-impaired-people

OCR and Text-to-Speech System

Overview

This Python script extracts text from an image using Optical Character Recognition (OCR) via Tesseract, summarizes the extracted text, and converts it into speech using pyttsx3. The script supports capturing an image using libcamera or uploading an existing image.

Features

Capture an image using libcamera

Upload an existing image file

Perform OCR on the image using pytesseract

Detect headers, footers, and body text

Identify page numbers in the extracted text

Detect text density to split images

Summarize extracted text using LSA (Latent Semantic Analysis)

Convert summarized text to speech using pyttsx3

Prerequisites

Ensure the following dependencies are installed:

Required Packages

pytesseract

Pillow

pyttsx3

sumy

tkinter

Install them using:

pip install pytesseract pillow pyttsx3 sumy

External Dependencies

Tesseract OCR

Install Tesseract:

Linux: sudo apt install tesseract-ocr

Windows: Download from Tesseract GitHub

Set pytesseract.pytesseract.tesseract_cmd to the correct Tesseract executable path

libcamera (For capturing images, required only on Raspberry Pi/Linux systems)

Install: sudo apt install libcamera-apps

Usage

Running the Script

python script.py

Options

Capture an image using libcamera

Upload an image from file

Input Format

Supported Image Formats: .jpg, .jpeg, .png, .bmp

Image should contain readable printed text for best results.

Output Format

Extracted text displayed on the console.

Summarized text printed to the console.

Summarized text is read aloud using pyttsx3.

Example Workflow

Select an option (Capture Image / Upload Image)

The script processes the image and extracts text

The extracted text is summarized

The summarized text is converted to speech and played

Version

Current Version: 1.0.0

Python Compatibility: Python 3.x

Known Issues

Handwritten text may not be accurately recognized.

Image quality impacts text extraction accuracy.

libcamera is required for capturing images on Linux; it won’t work on Windows.

