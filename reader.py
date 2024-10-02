import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from currency import Automaton
import xml.etree.ElementTree as ET

# Project imports
from extracts import extract_text_from_html, extract_text_from_xlsx, extract_text_from_csv, extract_text_from_docx
from saves import save_to_xlsx, save_to_csv


automaton = Automaton("currency_auto.xml")
symbols = ['$', '€', '¥', 'USD', 'EUR', 'MXN']
currencies = []

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

def analyze_text(text):
    global currencies
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

    position = 0

    for index, char in enumerate(text):
        print(f"Índice: {index}, Carácter: '{char}'")

    for i in range(len(text_array)):
        word = text_array[i]
        start_position = text.find(word, position)  
        end_position = start_position + len(word) - 1  
        position = end_position + 1  

        if word in symbols:
            symbol_index = i
            if evaluate_word(text_array[symbol_index-1] + ' ' + word):
                prev_word = text_array[symbol_index-1] # El número antes del simbolo (word es el simbolo)
                start_position = text.find(prev_word) # Aqui estoy buscando el numero ya que este es el caso donde el num esta antes del simbolo entonces del primer digito del num sale la pos de inicio diosmio
                end_position = start_position + len(prev_word + ' ' + word) - 1 
                currencies.append((prev_word + ' ' + word, start_position, end_position, i))
                continue

            if evaluate_word(word + ' ' + text_array[symbol_index+1]):
                next_word = text_array[symbol_index+1]
                end_position = start_position + len(word + ' ' + next_word) - 1  
                print(word + ' ' + next_word)
                currencies.append((word + ' ' + next_word, start_position, end_position, i))
                continue

        elif evaluate_word(word):
            currencies.append((word, start_position, end_position, i))

    display_results(currencies)

def display_results(currencies):
    result_text.delete(1.0, tk.END)
    
    for currency, start_position, end_position, word_index in currencies:
        result_text.insert(tk.END, f"{currency} | Posición inicial: {start_position}, Posición final: {end_position}, Índice de palabra: {word_index}\n")

    csv_button.pack(pady=5)
    xlsx_button.pack(pady=5)

root = tk.Tk()
root.title("Analizador de Monedas")

select_frame = tk.Frame(root)
select_frame.pack(pady=10)

label = tk.Label(select_frame, text="Seleccione un archivo para analizar:")
label.pack(side=tk.LEFT)

select_button = tk.Button(select_frame, text="Seleccionar archivo", command=process_file)
select_button.pack(side=tk.LEFT, padx=10)

result_frame = tk.Frame(root)
result_frame.pack(pady=10)

result_text = tk.Text(result_frame, height=20, width=80)
result_text.pack()

csv_button = tk.Button(root, text="Descargar CSV", command=lambda: save_to_csv(currencies))
xlsx_button = tk.Button(root, text="Descargar XLSX", command=lambda: save_to_xlsx(currencies))

root.mainloop()