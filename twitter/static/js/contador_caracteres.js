// contador_caracteres.js

document.addEventListener("DOMContentLoaded", function () {
    var textArea = document.getElementById("id_text");  // Ajusta el ID según el que tengas en tu formulario
    var charCountArea = document.getElementById("charCountArea");
    var tweetButton = document.getElementById("tweetButton");  // Ajusta el ID según el que tengas en tu botón

    // Inicializa el contador con la longitud máxima permitida
    var maxChars = 140;
    var currentChars = textArea.value.length;
    var remainingChars = maxChars - currentChars;
    charCountArea.textContent = remainingChars;

    // Actualiza el contador cuando se escriba en el área de texto
    textArea.addEventListener("input", function () {
        currentChars = textArea.value.length;
        remainingChars = maxChars - currentChars;
        charCountArea.textContent = remainingChars;

        // Deshabilita el botón si el número de caracteres es menor o igual a 0
        tweetButton.disabled = remainingChars <= 0;
    });
});
