const imageInput = document.getElementById('image-input');
const originalImage = document.getElementById('original-image');
const convertedImage = document.getElementById('converted-image');
const uploadButton = document.getElementById('upload-button');
const convertButton = document.getElementById('convert-button');

uploadButton.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
        originalImage.src = event.target.result;
    };

    reader.readAsDataURL(file);
});

convertButton.addEventListener('click', () => {
    // Преобразование изображения (для примера просто отражаем изображение)
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = originalImage.width;
    canvas.height = originalImage.height;

    ctx.drawImage(originalImage, 0, 0);
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);

    convertedImage.src = canvas.toDataURL();
});

