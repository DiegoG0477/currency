def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    words = text.split()
    
    return ' '.join(words)