// Funcionalidad para colorear SVG y selector de imagen
let selectedColor = null;

function updateColorButtonsState(selectedButton) {
    document.querySelectorAll('.color-button').forEach(btn => {
        btn.classList.remove('selected');
    });
    if (selectedButton) {
        selectedButton.classList.add('selected');
    }
}

document.querySelectorAll('.color-button').forEach(btn => {
    btn.addEventListener('click', () => {
        selectedColor = btn.getAttribute('data-color');
        updateColorButtonsState(btn);
    });
});

function attachColoringEvents() {
    document.querySelectorAll('.colorable').forEach(part => {
        part.addEventListener('click', () => {
            if (selectedColor) {
                part.setAttribute('fill', selectedColor);
            } else {
                alert("Por favor, selecciona un color primero");
            }
        });
    });
}

document.getElementById('image-selector').addEventListener('change', function() {
    const selectedImage = this.value;
    fetch(`assets/images/${selectedImage}`)
        .then(response => response.text())
        .then(svgContent => {
            document.getElementById('drawing').innerHTML = svgContent;
            attachColoringEvents();
        });
});

function clearColors() {
    document.querySelectorAll('.colorable').forEach(part => {
        part.setAttribute('fill', 'white');
    });
}

function saveDrawing() {
    html2canvas(document.getElementById('drawing')).then(canvas => {
        const link = document.createElement('a');
        link.download = 'mi_dibujo.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}

document.getElementById('image-selector').dispatchEvent(new Event('change'));
