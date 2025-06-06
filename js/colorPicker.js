let selectedColor = null;

function updateColorButtonsState(selectedButton) {
  const colorSquare = document.getElementById("selected-color-square");
  if (colorSquare) {
    colorSquare.style.backgroundColor = selectedColor || "white";
  }

  document.querySelectorAll(".color-button").forEach((btn) => {
    btn.style.transform = btn === selectedButton ? "scale(1.2)" : "scale(1)";
    btn.style.boxShadow =
      btn === selectedButton ? "0 0 10px rgba(0,0,0,0.3)" : "none";
  });
}

export function initColorPicker() {
  document.querySelectorAll(".color-button").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectedColor = btn.getAttribute("data-color");
      updateColorButtonsState(btn);
    });
  });
}

export function getSelectedColor() {
  return selectedColor;
}
