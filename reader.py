import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from currency import Automaton
import xml.etree.ElementTree as ET
from tkinter import ttk

# Project imports
from extracts import extract_text_from_html, extract_text_from_xlsx, extract_text_from_csv, extract_text_from_docx
from saves import save_to_xlsx, save_to_csv


automaton = Automaton("automaton.xml")
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
        data = extract_text_from_html(file_path)
    elif extension == 'xlsx':
        data = extract_text_from_xlsx(file_path)
    elif extension == 'csv':
        data = extract_text_from_csv(file_path)
    elif extension == 'docx':
        data = extract_text_from_docx(file_path)
    else:
        messagebox.showerror("Error", "Formato de archivo no soportado")
        return
    
    analyze_text(data, extension)

def analyze_text(data, extension):
    global currencies

    if extension == 'csv' or extension == 'xlsx':
        currencies = analyze_dataframe(data)
        update_treeview_for_csv()
    else:
        currencies = analyze_text_array(data)
        update_treeview_for_text()

    display_results(currencies, extension)

def evaluate_word(word): 
        current_state = automaton.initial_state
        for char in word:
            next_state = automaton.is_valid_transition(current_state, char)
            if next_state is None:
                return False
            current_state = next_state
        return current_state in automaton.final_states

def analyze_text_array(text):
    text_array = text.split(' ')
    currencies = []

    position = 0

    # for index, char in enumerate(text):
    #     print(f"Índice: {index}, Carácter: '{char}'")

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

    # display_results(currencies)
    return currencies

def analyze_dataframe(df):
    global currencies
    currencies = []

    def process_row(row, row_index):
        for col_index, value in row.items():
            if not pd.isna(value):
                process_cell(value, row_index, col_index)

    def process_cell(value, row_index, col_index):
        value_str = str(value)
        for symbol in symbols:
            if symbol in value_str and evaluate_word(value_str):
                currencies.append((value_str, row_index + 2, col_index))

    for row_index, row in df.iterrows():
        process_row(row, row_index)

    return currencies

def update_treeview_for_csv():
    tree["columns"] = ("Moneda", "Fila", "Columna")

    tree.heading("Moneda", text="Moneda")
    tree.heading("Fila", text="Fila")
    tree.heading("Columna", text="Columna")

    tree.column("Moneda", anchor="center")
    tree.column("Fila", anchor="center")
    tree.column("Columna", anchor="center")

def update_treeview_for_text():
    tree["columns"] = ("Moneda", "Posición inicial", "Posición final", "Índice")

    tree.heading("Moneda", text="Moneda")
    tree.heading("Posición inicial", text="Posición inicial")
    tree.heading("Posición final", text="Posición final")
    tree.heading("Índice", text="Índice")

    tree.column("Moneda", anchor="center")
    tree.column("Posición inicial", anchor="center")
    tree.column("Posición final", anchor="center")
    tree.column("Índice", anchor="center")

def display_results(currencies, extension):
    for row in tree.get_children():
        tree.delete(row)

    for currency in currencies:
        if extension == 'csv' or extension == 'xlsx':
            value, row_index, col_index = currency
            tree.insert("", tk.END, values=(value, row_index, col_index))
        else:
            value, start_position, end_position, word_index = currency
            tree.insert("", tk.END, values=(value, start_position, end_position, word_index))

    csv_button.pack(pady=5)
    xlsx_button.pack(pady=5)

root = tk.Tk()
root.title("Analizador de Monedas")
root.configure(bg="#ADD8E6")

title_frame = tk.Frame(root, bg="#ADD8E6")
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="Currency", font=("Arial", 16, "bold"), bg="#ADD8E6", fg="#00008B")
title_label.pack(padx=5)  

subtitle_label = tk.Label(title_frame, text="Reconocedor de diferentes concurrencias monetarias", font=("Arial", 10), bg="#ADD8E6", fg="#00008B")
subtitle_label.pack(padx=5)  

select_frame = tk.Frame(root, bg="#ADD8E6")
select_frame.pack(pady=10)

label = tk.Label(select_frame, text="Seleccione un archivo para analizar:", bg="#ADD8E6", fg="#00008B")
label.pack(side=tk.LEFT)

select_button = tk.Button(select_frame, text="Seleccionar archivo", command=process_file, bg="white", fg="#00008B")
select_button.pack(side=tk.LEFT, padx=10)

result_frame = tk.Frame(root, bg="#ADD8E6")
result_frame.pack(pady=10)

columns = ("Moneda", "Posición inicial", "Posición final", "Índice")
tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20)
tree.pack()

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")  

footer_label = tk.Label(root, text="Integrantes: Diego Gordillo L - 223213 Mónica Mundo C - 223238", font=("Arial", 10), bg="#ADD8E6", fg="#00008B")
footer_label.pack(side=tk.LEFT, padx=10, pady=10)

csv_button = tk.Button(root, text="Descargar CSV", command=lambda: save_to_csv(currencies), bg="white", fg="#00008B")
xlsx_button = tk.Button(root, text="Descargar XLSX", command=lambda: save_to_xlsx(currencies), bg="white", fg="#00008B")

root.mainloop()