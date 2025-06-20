import os
import base64
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image

class PNGtoSVGConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conversor PNG a SVG")
        self.root.geometry("600x400")
        
        # Carpetas por defecto
        self.input_folder = Path("input")
        self.output_folder = Path("procesamiento_svg")
        
        # Crear carpetas si no existen
        self.input_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Conversor PNG a SVG", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Información de carpetas
        info_frame = ttk.LabelFrame(main_frame, text="Configuración de Carpetas", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Carpeta de entrada: {self.input_folder}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"Carpeta de salida: {self.output_folder}").grid(row=1, column=0, sticky=tk.W)
        
        # Botones de selección
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Button(buttons_frame, text="Seleccionar Archivos PNG", 
                  command=self.select_files, width=25).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="Procesar Carpeta Input", 
                  command=self.process_input_folder, width=25).grid(row=0, column=1)
        
        # Área de texto para mostrar progreso
        self.text_area = tk.Text(main_frame, height=15, width=70)
        self.text_area.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para el área de texto
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        # Configurar redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def log_message(self, message):
        """Agregar mensaje al área de texto"""
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.root.update()
    
    def png_to_svg(self, png_path, svg_path):
        """Convertir PNG a SVG embebido"""
        try:
            # Abrir imagen PNG
            with Image.open(png_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Obtener dimensiones
                width, height = img.size
                
                # Convertir a base64
                with open(png_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                
                # Crear SVG
                svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <image x="0" y="0" width="{width}" height="{height}" 
           xlink:href="data:image/png;base64,{img_data}"/>
</svg>'''
                
                # Guardar SVG
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                return True
        except Exception as e:
            self.log_message(f"Error al convertir {png_path}: {str(e)}")
            return False
    
    def select_files(self):
        """Seleccionar archivos PNG específicos"""
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PNG",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if files:
            self.log_message(f"Seleccionados {len(files)} archivos para convertir...")
            converted = 0
            
            for file_path in files:
                png_path = Path(file_path)
                svg_name = png_path.stem + ".svg"
                svg_path = self.output_folder / svg_name
                
                self.log_message(f"Convirtiendo: {png_path.name}")
                
                if self.png_to_svg(png_path, svg_path):
                    converted += 1
                    self.log_message(f"✓ Convertido: {svg_path}")
                else:
                    self.log_message(f"✗ Error al convertir: {png_path.name}")
            
            self.log_message(f"\n--- Conversión completada ---")
            self.log_message(f"Archivos convertidos: {converted}/{len(files)}")
            messagebox.showinfo("Completado", f"Se convirtieron {converted} de {len(files)} archivos")
    
    def process_input_folder(self):
        """Procesar todos los PNG en la carpeta input"""
        if not self.input_folder.exists():
            messagebox.showerror("Error", f"La carpeta {self.input_folder} no existe")
            return
        
        # Buscar archivos PNG
        png_files = list(self.input_folder.glob("*.png"))
        png_files.extend(list(self.input_folder.glob("*.PNG")))
        
        if not png_files:
            messagebox.showwarning("Advertencia", f"No se encontraron archivos PNG en {self.input_folder}")
            return
        
        self.log_message(f"Encontrados {len(png_files)} archivos PNG en la carpeta input...")
        converted = 0
        
        for png_path in png_files:
            svg_name = png_path.stem + ".svg"
            svg_path = self.output_folder / svg_name
            
            self.log_message(f"Convirtiendo: {png_path.name}")
            
            if self.png_to_svg(png_path, svg_path):
                converted += 1
                self.log_message(f"✓ Convertido: {svg_path}")
            else:
                self.log_message(f"✗ Error al convertir: {png_path.name}")
        
        self.log_message(f"\n--- Conversión completada ---")
        self.log_message(f"Archivos convertidos: {converted}/{len(png_files)}")
        messagebox.showinfo("Completado", f"Se convirtieron {converted} de {len(png_files)} archivos")
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PNGtoSVGConverter()
    app.run()