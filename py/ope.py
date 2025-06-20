import cv2
import numpy as np
import svgwrite
import os

def contour_to_svg_path(cnt):
    path_str = "M {} {}".format(cnt[0][0][0], cnt[0][0][1])
    for pt in cnt[1:]:
        path_str += " L {} {}".format(pt[0][0], pt[0][1])
    path_str += " Z"
    return path_str

def png_to_svg_zonas(input_path, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4:
        alpha = img[:,:,3]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        img_gray[alpha == 0] = 255
    else:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    h, w = binary.shape
    dwg = svgwrite.Drawing(output_path, size=(w, h))
    for i, cnt in enumerate(contours):
        if hierarchy[0][i][3] == -1:
            path = contour_to_svg_path(cnt)
            dwg.add(
                dwg.path(
                    d=path,
                    fill="#ffffff",
                    stroke="#000000",
                    stroke_width=2,
                    id=f"zona_{i}"
                )
            )
    dwg.save()
    print(f"✅ SVG generado: {output_path}")

def procesar_archivos(origen_folder, destino_folder):
    # Listar archivos PNG en la carpeta de origen
    files = [f for f in os.listdir(origen_folder) if f.lower().endswith('.png')]
    if not files:
        print("No se encontraron archivos PNG en la carpeta 'input'.")
        return

    print("Archivos encontrados:")
    for idx, file in enumerate(files):
        print(f"{idx+1}. {file}")

    print("\nSelecciona un archivo por número o '0' para procesar TODOS:")
    seleccion = input("Número: ")
    if seleccion == "0":
        seleccionados = files
    else:
        try:
            idx = int(seleccion) - 1
            seleccionados = [files[idx]]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

    for file in seleccionados:
        nombre_sin_ext = os.path.splitext(file)[0]
        input_path = os.path.join(origen_folder, file)
        output_path = os.path.join(destino_folder, f"{nombre_sin_ext}.svg")
        png_to_svg_zonas(input_path, output_path)

def main():
    origen_folder = "input"
    destino_folder = "procesamiento_svg"
    # Crear carpetas si no existen
    os.makedirs(origen_folder, exist_ok=True)
    os.makedirs(destino_folder, exist_ok=True)
    print(f"\nColoca tus archivos PNG en la carpeta '{origen_folder}/' antes de continuar.")
    procesar_archivos(origen_folder, destino_folder)

if __name__ == "__main__":
    main()
