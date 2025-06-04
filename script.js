let selectedColor = null;
document.querySelectorAll('.color').forEach(btn => {
    btn.addEventListener('click', () => {
        selectedColor = btn.getAttribute('data-color');
    });
});
function attachColoringEvents() {
    document.querySelectorAll('.colorable').forEach(part => {
        part.addEventListener('click', () => {
            if (selectedColor) {
                part.setAttribute('fill', selectedColor);
            } else {
                alert("Selecciona un color primero.");
            }
        });
    });
}
document.getElementById('image-selector').addEventListener('change', function() {
    const selectedImage = this.value;
    fetch(`assets/images/${selectedImage}`)
        .then(response => response.text())
        .then(svgContent => {
            document.getElementById('drawing-container').innerHTML = svgContent;
            attachColoringEvents();
        });
});
function clearColors() {
    document.querySelectorAll('.colorable').forEach(part => {
        part.setAttribute('fill', 'white');
    });
}
function saveDrawing() {
    html2canvas(document.getElementById('drawing-container')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'mi_dibujo.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}
document.getElementById('image-selector').dispatchEvent(new Event('change'));
