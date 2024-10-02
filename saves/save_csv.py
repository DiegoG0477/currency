from tkinter import filedialog, messagebox
import pandas as pd

def save_to_csv(currencies):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        if not currencies:
            messagebox.showwarning("Advertencia", "No hay datos para guardar.")
            return
        
        df = pd.DataFrame(currencies, columns=["Moneda", "Posición Inicial", "Posición Final", "Indice"])

        try:
            df.to_csv(save_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Guardado", f"Resultados guardados en {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")