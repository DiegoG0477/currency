import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from bs4 import BeautifulSoup
import docx
from currency import Automaton
import xml.etree.ElementTree as ET

# Project imports
from html_extract import extract_text_from_html

automaton = Automaton("currency_auto.xml")
symbols = ['$', '€', '¥', 'USD', 'EUR', 'MXN']

def process_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.xlsx *.csv *.docx *.html"), 
                                                      ("Excel files", "*.xlsx"), 
                                                      ("CSV files", "*.csv"), 
                                                      ("Word files", "*.docx"), 
                                                      ("HTML files", "*.html")])
    
    if not file_path:
        return

    extension = file_path.split('.')[-1].lower()

    if extension == 'html':
        text = extract_text_from_html(file_path)
    elif extension == 'xlsx':
        text = extract_text_from_xlsx(file_path)
    elif extension == 'csv':
        text = extract_text_from_csv(file_path)
    elif extension == 'docx':
        text = extract_text_from_docx(file_path)
    else:
        messagebox.showerror("Error", "Formato de archivo no soportado")
        return
    
    analyze_text(text)

def extract_text_from_xlsx(file_path):
    df = pd.read_excel(file_path)
    text = ' '.join(df.astype(str).stack().tolist())
    print(text)
    return text

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    text = ' '.join(df.astype(str).stack().tolist())
    print(text)
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return ' '.join(full_text)

def analyze_text(text):
    text_array = text.split(' ')
    currencies = []
    def evaluate_word(word): 
        current_state = automaton.initial_state
        for char in word:
            next_state = automaton.is_valid_transition(current_state, char)
            if next_state is None:
                return False
            current_state = next_state
        return current_state in automaton.final_states
    for i in range(len(text_array)):
        current_state = automaton.initial_state
        word = text_array[i]
        if word in symbols:
            symbol_index = i
            if evaluate_word(text_array[symbol_index-1] + ' ' + word):
                currencies.append(text_array[symbol_index-1] + ' ' + word)
                continue
            if evaluate_word(word + ' ' + text_array[symbol_index+1]):
                currencies.append(word + ' ' + text_array[symbol_index+1])
        elif evaluate_word(word):
            currencies.append(word)
    display_results(currencies)

def display_results(currencies):
    result_window = tk.Toplevel()
    result_window.title("Resultados encontrados")
    result_text = tk.Text(result_window, height=20, width=80)
    result_text.pack()
    result_text.insert(tk.END, '\n'.join(currencies))
    save_button = tk.Button(result_window, text="Descargar resultados", command=lambda: save_to_xlsx(currencies))
    save_button.pack()

def save_to_xlsx(currencies):
    df = pd.DataFrame(currencies, columns=["Monedas encontradas"])
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Guardado", f"Resultados guardados en {save_path}")


root = tk.Tk()
root.title("Analizador de Monedas")

label = tk.Label(root, text="Seleccione un archivo para analizar:")
label.pack(pady=10)

select_button = tk.Button(root, text="Seleccionar archivo", command=process_file)
select_button.pack(pady=10)

root.mainloop()
