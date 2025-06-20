import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import potracer
import xml.etree.ElementTree as ET


def convert_png_to_svg(input_path, output_folder):
    """Convierte una imagen PNG a SVG usando potracer."""
    try:
        # Abrir imagen y asegurar escala de grises o binaria
        image = Image.open(input_path).convert("L")  # Escala de grises
        image = image.point(lambda x: 0 if x < 128 else 255, "1")  # Binarizar

        # Guardar temporal como PBM (formato soportado por potracer)
        temp_pbm = os.path.join(output_folder, "__temp.pbm")
        image.save(temp_pbm)

        # Usar potracer para trazar el SVG
        svg_data = potracer.image2svg(temp_pbm, mode='center', opttolerance=0.2)

        # Limpiar archivo temporal
        os.remove(temp_pbm)

        # Guardar resultado SVG
        filename = os.path.splitext(os.path.basename(input_path))[0] + ".svg"
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_data)

        print(f"[OK] Convertido: {input_path} -> {output_path}")

    except Exception as e:
        print(f"[ERROR] No se pudo convertir {input_path}: {e}")


def process_files(input_paths, output_folder):
    """Procesa archivos o carpetas seleccionadas."""
    os.makedirs(output_folder, exist_ok=True)

    for input_path in input_paths:
        if os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(".png"):
                        full_path = os.path.join(root, file)
                        convert_png_to_svg(full_path, output_folder)
        elif os.path.isfile(input_path) and input_path.lower().endswith(".png"):
            convert_png_to_svg(input_path, output_folder)
        else:
            print(f"[SKIP] Archivo no válido o no es PNG: {input_path}")


def select_files_or_folders():
    """Abre diálogo para seleccionar archivos o carpetas."""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    paths = filedialog.askopenfilenames(
        title="Selecciona archivos PNG o carpetas",
        filetypes=[("PNG Files or Folders", "*.*")]
    )
    return paths


if __name__ == "__main__":
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "procesamiento_svg"

    os.makedirs(INPUT_FOLDER, exist_ok=True)

    selected_paths = select_files_or_folders()
    if not selected_paths:
        messagebox.showinfo("Info", "No se seleccionaron archivos.")
    else:
        process_files(selected_paths, OUTPUT_FOLDER)
        messagebox.showinfo("Completado", f"Archivos procesados guardados en: {OUTPUT_FOLDER}")