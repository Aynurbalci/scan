import pytesseract
import sys
from scanner import config

sys.path.insert(0, str(config.ROOT_DIR))


def perform_ocr(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return None #logla spesifik al



def validate_address(address):
    keywords = ["sokak", "cadde", "mahalle", "bina", "apartman", "köy", "şehir", "ilçe", "ülke"]
    for keyword in keywords:
        if keyword in address.lower():
            return True
    return False


def is_meaningful_content(content, non_zero_threshold=0.8):
    total_characters = len(content)
    zero_characters = sum(1 for char in content if char == '0')
    non_zero_characters = total_characters - zero_characters
    non_zero_ratio = non_zero_characters / total_characters
    return non_zero_ratio >= non_zero_threshold


def validate_credit_card(card_number):
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit():
        return False

    digits = list(map(int, card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    total = sum(odd_digits)

    for digit in even_digits:
        double_digit = digit * 2
        if double_digit > 9:
            double_digit -= 9
        total += double_digit

    return total % 10 == 0

