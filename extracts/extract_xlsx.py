import pandas as pd

def extract_text_from_xlsx(file_path):
    df = pd.read_excel(file_path)
    text = ' '.join(df.astype(str).stack().tolist())
    print(text)
    return text