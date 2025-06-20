import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import subprocess
import tempfile

def seleccionar_entrada():
    root = tk.Tk()
    root.withdraw()
    
    opcion = messagebox.askquestion(
        "Selección",
        "¿Desea procesar archivos individuales o una carpeta completa?",
        icon='question',
        type='yesno'
    )
    
    if opcion == 'yes':
        archivos = filedialog.askopenfilenames(
            title="Seleccione los archivos PNG a convertir",
            initialdir="input",
            filetypes=(("Archivos PNG", "*.png"), ("Todos los archivos", "*.*"))
        )
        return list(archivos)
    else:
        carpeta = filedialog.askdirectory(
            title="Seleccione la carpeta con archivos PNG",
            initialdir="input"
        )
        if carpeta:
            archivos = []
            for root, dirs, files in os.walk(carpeta):
                for file in files:
                    if file.lower().endswith('.png'):
                        archivos.append(os.path.join(root, file))
            return archivos
    return []

def convertir_png_a_svg(archivo_png, carpeta_salida):
    try:
        nombre_base = os.path.splitext(os.path.basename(archivo_png))[0]
        archivo_svg = os.path.join(carpeta_salida, f"{nombre_base}.svg")
        
        # Crear un archivo temporal BMP (potrace trabaja mejor con BMP)
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as tmp_bmp:
            # Convertir PNG a BMP
            with Image.open(archivo_png) as img:
                img.save(tmp_bmp.name, format='BMP')
            
            # Usar potrace para convertir BMP a SVG
            subprocess.run([
                'potrace',
                tmp_bmp.name,
                '-s',  # Salida SVG
                '-o', archivo_svg
            ], check=True)
            
        # Eliminar el archivo temporal
        os.unlink(tmp_bmp.name)
        
        return True
    except Exception as e:
        print(f"Error al convertir {archivo_png}: {str(e)}")
        return False

def procesar_archivos():
    os.makedirs("input", exist_ok=True)
    os.makedirs("procesamiento_svg", exist_ok=True)
    
    archivos = seleccionar_entrada()
    
    if not archivos:
        messagebox.showinfo("Información", "No se seleccionaron archivos para procesar")
        return
    
    exitos = 0
    for archivo in archivos:
        if convertir_png_a_svg(archivo, "procesamiento_svg"):
            exitos += 1
    
    messagebox.showinfo(
        "Proceso completado",
        f"Conversión finalizada:\n\nArchivos procesados: {len(archivos)}\nConversiones exitosas: {exitos}"
    )

if __name__ == "__main__":
    try:
        from PIL import Image
        # Verificar si potrace está instalado
        subprocess.run(['potrace', '--version'], capture_output=True, check=True)
    except ImportError:
        print("Por favor instale Pillow: pip install pillow")
        exit(1)
    except subprocess.CalledProcessError:
        print("Potrace no está instalado. Por favor instálelo:")
        print("Windows: Descargar de https://potrace.sourceforge.net/")
        print("Linux (Ubuntu/Debian): sudo apt-get install potrace")
        print("macOS (Homebrew): brew install potrace")
        exit(1)
    
    procesar_archivos()