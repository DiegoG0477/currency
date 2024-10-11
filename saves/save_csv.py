from tkinter import filedialog, messagebox
import pandas as pd

def save_to_csv(currencies):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        if not currencies:
            messagebox.showwarning("Advertencia", "No hay datos para guardar.")
            return
        
        csv_columns = []
        
        if len(currencies[0]) == 3:
            csv_columns = ['Moneda', 'Fila', 'Columna']
        else:
            csv_columns = ["Moneda", "Posición Inicial", "Posición Final"]
        
        df = pd.DataFrame(currencies, columns=csv_columns)

        try:
            df.to_csv(save_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Guardado", f"Resultados guardados en {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")