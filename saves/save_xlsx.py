from tkinter import filedialog, messagebox
import pandas as pd

def save_to_xlsx(currencies):
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        if not currencies:
            messagebox.showwarning("Advertencia", "No hay datos para guardar.")
            return
        
        df = pd.DataFrame(currencies, columns=["Moneda", "Posición Inicial", "Posición Final", "Indice"])
        
        try:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Guardado", f"Resultados guardados en {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")