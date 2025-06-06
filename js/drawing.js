import { getSelectedColor } from './colorPicker.js';

export function attachColoringEvents() {
    document.querySelectorAll('.colorable').forEach(part => {
        part.addEventListener('click', () => {
            const selectedColor = getSelectedColor();
            if (selectedColor) {
                part.setAttribute('fill', selectedColor);
            } else {
                alert("Por favor, selecciona un color primero");
                document.querySelector('.color-palette').style.animation = 'highlight 1s';
                setTimeout(() => {
                    document.querySelector('.color-palette').style.animation = '';
                }, 1000);
            }
        });
    });
}

export function clearColors() {
    document.querySelectorAll('.colorable').forEach(part => {
        part.setAttribute('fill', 'white');
    });
}

export function saveDrawing() {
    html2canvas(document.getElementById('drawing-container')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'mi_dibujo.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}