let selectedColor = null;

// Función para actualizar el estado visual de los botones de color
function updateColorButtonsState(selectedButton) {
    // Actualizar el cuadrado indicador
    const colorSquare = document.getElementById('selected-color-square');
    if (colorSquare) {
        colorSquare.style.backgroundColor = selectedColor || 'white';
    }

    // Actualizar estado visual de los botones
    document.querySelectorAll('.color-button').forEach(btn => {
        btn.style.transform = btn === selectedButton ? 'scale(1.2)' : 'scale(1)';
        btn.style.boxShadow = btn === selectedButton ? '0 0 10px rgba(0,0,0,0.3)' : 'none';
    });
}

// Agregar eventos a los botones de color
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
                // Resaltar la paleta de colores
                document.querySelector('.color-palette').style.animation = 'highlight 1s';
                setTimeout(() => {
                    document.querySelector('.color-palette').style.animation = '';
                }, 1000);
            }
        });
    });
}

// Agregar estilos de animación al head
const style = document.createElement('style');
style.textContent = `
    @keyframes highlight {
        0% { transform: scale(1); box-shadow: none; }
        50% { transform: scale(1.05); box-shadow: 0 0 15px rgba(0,0,0,0.2); }
        100% { transform: scale(1); box-shadow: none; }
    }
`;
document.head.appendChild(style);

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
