letter_eq = {
    'ə': 'a',
    'ğ': 'gh',
    'ü': 'u',
    'ş': 'sh',
    'ı': 'i',
    'ç': 'ch',
    'ö': 'o',
}

def convert_slug(text):
    result = ''
    for char in text.lower():
        if char.isalnum():
            result += letter_eq.get(char, char)
        if char.isspace():
            result += '-'
    return result