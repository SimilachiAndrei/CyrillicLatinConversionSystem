import re


def romanian_cyrillic_to_latin(text):
    """Transliterate Romanian Cyrillic text to Latin alphabet."""

    # Create the transliteration dictionary
    translit_dict = {
        # Single character mappings
        'А': 'a', 'а': 'a',
        'Б': 'b', 'б': 'b',
        'В': 'v', 'в': 'v',
        'Г': 'g', 'г': 'g',
        'Д': 'd', 'д': 'd',
        'Є': 'e', 'є': 'e',
        'Е': 'e', 'е': 'e',
        'Ж': 'j', 'ж': 'j',
        'Ѕ': 'dz', 'ѕ': 'dz',
        'З': 'z', 'з': 'z',
        'И': 'i', 'и': 'i',
        'Й': 'i', 'й': 'i',
        'І': 'i', 'і': 'i',
        'К': 'c', 'к': 'c',
        'Л': 'l', 'л': 'l',
        'М': 'm', 'м': 'm',
        'Н': 'n', 'н': 'n',
        'Ѻ': 'o', 'ѻ': 'o',
        'О': 'o', 'о': 'o',
        'П': 'p', 'п': 'p',
        'Р': 'r', 'р': 'r',
        'С': 's', 'с': 's',
        'Т': 't', 'т': 't',
        'ОУ': 'u', 'оу': 'u',
        'Оу': 'u', 'Ȣ': 'u',
        'У': 'u', 'у': 'u',
        'Ф': 'f', 'ф': 'f',
        'Х': 'h', 'х': 'h',
        'Ѡ': 'o', 'ѡ': 'o',
        'Щ': 'șt', 'щ': 'șt',
        'Ц': 'ț', 'ц': 'ț',
        'Ч': 'c', 'ч': 'c',
        'Ш': 'ș', 'ш': 'ș',
        'Ъ': 'ă', 'ъ': 'ă',
        'Ы': 'â', 'ы': 'â',
        'Ꙑ': 'â', 'ꙑ': 'â',
        'Ь': 'ă', 'ь': 'ă',
        'Ѣ': 'ea', 'ѣ': 'ea',
        'Ю': 'iu', 'ю': 'iu',
        'Ꙗ': 'ia', 'ꙗ': 'ia',
        'Ѥ': 'ie', 'ѥ': 'ie',
        'Ѧ': 'ea', 'ѧ': 'ea',
        'Ѫ': 'î', 'ѫ': 'î',
        'Ѯ': 'x', 'ѯ': 'x',
        'Ѱ': 'ps', 'ѱ': 'ps',
        'Ѳ': 't', 'ѳ': 't',
        'Ѵ': 'i', 'ѵ': 'i',
        'Ꙟ': 'în', 'ꙟ': 'în',
        '↑': 'îm',
        'Џ': 'g', 'џ': 'g',

        # Multi-character sequences that need special handling
        'оу': 'u', 'Оу': 'u', 'ОУ': 'u',
    }

    # Handle special cases with context (like gh/ch/gi/ci)
    # We'll process these after the initial transliteration

    # First, replace multi-character sequences
    text = re.sub(r'([Оо])у', 'u', text)
    text = re.sub(r'([Оо])У', 'u', text)
    text = re.sub(r'([ОО])у', 'u', text)

    # Then replace single characters
    for cyr, lat in translit_dict.items():
        text = text.replace(cyr, lat)

    # Handle context-sensitive transliterations
    # g → gh before e/i
    text = re.sub(r'g([ei])', r'gh\1', text)
    # c → ch before e/i
    text = re.sub(r'c([ei])', r'ch\1', text)
    # g → gi before e/i (for џ)
    text = re.sub(r'g([ei])', r'gi\1', text)
    # c → ci before e/i (for ч)
    text = re.sub(r'c([ei])', r'ci\1', text)

    return text

if __name__ == "__main__":
    try:
        for i in range(1, 379):
            text_path = "data/text_catehism/" + str(i) + ".txt"
            with open(text_path, "r", encoding="utf-8") as f:
                cyrillic_text = f.read()
            latin_text = romanian_cyrillic_to_latin(cyrillic_text)
            latin_path = "data/transliterated_catehism/" + str(i) + ".txt"
            with open(latin_path, "w", encoding="utf-8") as f:
                f.write(latin_text)
    except Exception as e:
        print(f"Error: {str(e)}")
