import pytesseract
from PIL import Image
import re


def image_to_cyrillic_text(image_path):
    """
    Extract Cyrillic text from a PNG image and prepare it for transliteration.

    Args:
        image_path (str): Path to the PNG image file

    Returns:
        str: Cleaned Cyrillic text ready for transliteration
    """
    # Load the image
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        raise ValueError(f"Image file not found: {image_path}")

    # Configure Tesseract for Cyrillic
    custom_config = r'--oem 3 --psm 6 -l ron+rus+bul'  # Romanian + Russian + Bulgarian

    # Perform OCR
    text = pytesseract.image_to_string(img, config=custom_config)

    # Clean the text (remove non-Cyrillic characters except punctuation and spaces)
    cyrillic_pattern = re.compile(
        r'[^\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\'".,!?;: -]'
    )
    cleaned_text = cyrillic_pattern.sub('', text)

    # Normalize whitespace
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text


if __name__ == "__main__":
    # Example usage
    image_path = "1.png"  # Change to your image path
    try:
        cyrillic_text = image_to_cyrillic_text(image_path)
        print("Extracted Cyrillic Text:")
        print(cyrillic_text)

        # Save to file for your transliterator
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(cyrillic_text)
        print("\nText saved to 'extracted_text.txt'")

    except Exception as e:
        print(f"Error: {str(e)}")