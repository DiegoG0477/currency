from tkinter import filedialog, messagebox
import pandas as pd

def save_to_xlsx(currencies):
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        if not currencies:
            messagebox.showwarning("Advertencia", "No hay datos para guardar.")
            return
        
        xlsx_columns = []

        if len(currencies[0]) == 3:
            xlsx_columns = ['Moneda', 'Fila', 'Columna']
        else:
            xlsx_columns = ["Moneda", "Posición Inicial", "Posición Final"]

        df = pd.DataFrame(currencies, columns=xlsx_columns)
        
        try:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Guardado", f"Resultados guardados en {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")