import { initColorPicker } from './colorPicker.js';
import { attachColoringEvents, clearColors, saveDrawing } from './drawing.js';

document.getElementById('image-selector').addEventListener('change', function() {
    const selectedImage = this.value;
    fetch(`assets/images/${selectedImage}`)
        .then(response => response.text())
        .then(svgContent => {
            document.getElementById('drawing-container').innerHTML = svgContent;
            attachColoringEvents();
        });
});

window.clearColors = clearColors;
window.saveDrawing = saveDrawing;

document.addEventListener('DOMContentLoaded', () => {
    initColorPicker();
    document.getElementById('image-selector').dispatchEvent(new Event('change'));
});