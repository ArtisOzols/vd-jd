const image_input = document.querySelector("#image_input");
const image_div = document.querySelector("#display_image")
const input = document.getElementById('input');
const output = document.getElementById('output');
const char_buttons = image_div.children[1];

image_input.addEventListener("change", function(){
  document.querySelector("#loading").style.display = "block";
  output.style.backgroundColor = "lightgray";
  output.style.opacity = "20%";
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_img = reader.result;
    image_div.style.backgroundImage = `url(${uploaded_img})`;
    char_buttons.style.display = "none";

    let image = new Image();
    image.src = reader.result;
    image.onload = function() {
      image_div.style.maxHeight = image.height + "px";
      
      // Creating canvas for Tesseract
      const canvasForTesseract = document.createElement('canvas');
      const ctxForTesseract = canvasForTesseract.getContext('2d');
      canvasForTesseract.width = image.width;
      canvasForTesseract.height = image.height;
      ctxForTesseract.drawImage(image, 0, 0);

      // Converting image to grayscale
      var imgData = ctxForTesseract.getImageData(0,0, image.width, image.height);
      for (var i = 0; i<imgData.data.length; i += 4) {
        var avg = (imgData.data[i]+imgData.data[i+1]+imgData.data[i+2])/3;
        imgData.data[i] = avg;
        imgData.data[i+1] = avg;
        imgData.data[i+2] = avg;
      }
      ctxForTesseract.putImageData(imgData, 0, 0, 0, 0, imgData.width, imgData.height);
      
      var dataURL = canvasForTesseract.toDataURL();
      image_to_text(dataURL);
    };
  });
  reader.readAsDataURL(this.files[0]);
});
async function image_to_text(img) {
  const worker = await Tesseract.createWorker("Frak_LV_280721_500k");
  const { data: { text } } = await worker.recognize(img);

  document.querySelector("#loading").style.display = "none";
  output.style.backgroundColor = "white";
  output.style.opacity = "100%";
  output.value = convert_text(text);  
};

function removeFiles() {
  image_input.value = "";
  input.value = "";
  input.focus();
  output.value = "";
  image_div.style.backgroundImage = "none";
  image_div.style.maxHeight = "unset";
  char_buttons.style.display = "flex";
}

function convert_text(text) {
  py_convert_text = pyscript.interpreter.globals.get('convert');
  return py_convert_text(text);
};


function set_output_val() {
  output.value = convert_text(input.value);
};

input.addEventListener('input', set_output_val)
set_output_val();

function addCharacter(char) {
  var curPos = input.selectionStart;
  let x = input.value;
  input.value = x.slice(0, curPos) + char + x.slice(curPos);
  set_output_val();
  input.focus();
}