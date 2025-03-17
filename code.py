import pyttsx3
import pytesseract
from PIL import Image
from tkinter import Tk, filedialog
import re
import os
import subprocess
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Configure Tesseract executable path (adjust if not using default path)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def capture_image_with_libcamera():
    """Capture an image using libcamera."""
    file_path = "captured_image.jpg"
    print("Capturing image using libcamera...")
    subprocess.run(["libcamera-still", "-o", file_path, "--timeout", "2000", "--width", "1024", "--height", "768"])
    if os.path.exists(file_path):
        print(f"Image captured and saved as {file_path}")
        return file_path
    else:
        print("Failed to capture image.")
        return None

def upload_image():
    """Open a file dialog to select an image."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return file_path

def extract_text(image):
    """Extract text from an image using Tesseract."""
    return pytesseract.image_to_string(image).strip()

def detect_header_and_footer(text):
    """Detect headers and footers in the extracted text."""
    lines = text.splitlines()
    header = None
    footer = None
    body_text = []

    if lines:
        # Detect header if the first line is short
        if len(lines[0]) < 50:
            header = lines[0]
            lines = lines[1:]

        # Detect footer if the last line is short
        if lines and len(lines[-1]) < 50:
            footer = lines[-1]
            lines = lines[:-1]

    body_text = '\n'.join(lines).strip()

    return {
        'header': header,
        'footer': footer,
        'body_text': body_text
    }

def detect_page_number_in_text(line):
    """Detects page number in a line if it's present at the start or end."""
    words = line.split()
    page_number = None

    if words:
        if re.match(r'^\d+$', words[0]):
            page_number = words[0]
        elif re.match(r'^\d+$', words[-1]):
            page_number = words[-1]

    return page_number

def find_split_position(image):
    """Find a split position based on text density."""
    width, height = image.size
    boxes = pytesseract.image_to_boxes(image)

    text_density = [0] * width
    for box in boxes.splitlines():
        b = box.split()
        x_left = int(b[1])
        x_right = int(b[3])
        for x in range(x_left, x_right):
            text_density[x] += 1

    split_position = width // 2
    min_density = min(text_density[width // 4: 3 * width // 4])
    for i in range(width // 4, 3 * width // 4):
        if text_density[i] == min_density:
            split_position = i
            break

    return split_position

def summarize_text(text):
    """Summarizes text using the LSA Summarizer."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summarized_sentences = summarizer(parser.document, 3)
    summary = ' '.join(str(sentence) for sentence in summarized_sentences)
    return summary

def text_to_speech(text):
    """Converts text to speech using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    print("Choose an option:")
    print("1. Capture image from camera (using libcamera)")
    print("2. Upload image from file")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        image_path = capture_image_with_libcamera()
    elif choice == '2':
        image_path = upload_image()
    else:
        print("Invalid choice!")
        return

    if image_path:
        print(f"Processing image: {image_path}")
        img = Image.open(image_path)

        split_position = find_split_position(img)
        print(f"Splitting the image at position: {split_position}")

        width, height = img.size
        left_image = img.crop((0, 0, split_position, height))
        right_image = img.crop((split_position, 0, width, height))

        left_text = extract_text(left_image)
        right_text = extract_text(right_image)

        left_sections = detect_header_and_footer(left_text)
        right_sections = detect_header_and_footer(right_text)

        print("\nBody Text from left section:\n", left_sections['body_text'])
        print("\nBody Text from right section:\n", right_sections['body_text'])

        # Summarize and speak the extracted body text
        combined_text = left_sections['body_text'] + "\n" + right_sections['body_text']
        summary = summarize_text(combined_text)
        print("\nSummarized Text:\n", summary)

        print("\nReading summarized text...")
        text_to_speech(summary)
    else:
        print("No image selected!")

if __name__ == "__main__":
    main()