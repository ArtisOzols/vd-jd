const input_btn = document.getElementById("img_input_btn"); // input that takes image
const img_btn_div = document.getElementById("img_btn_div"); // button that sets value to input_btn
const input = document.getElementById('input');
const output = document.getElementById('output');
const char_buttons = document.getElementById('character_buttons');
const canvasForHtml = document.getElementById("img_canvas");
const ctxForHtml = canvasForHtml.getContext('2d');


input_btn.addEventListener("change", function(){
  document.getElementById("loading").style.display = "block";
  output.style.backgroundColor = "lightgray";
  output.style.opacity = "20%";
  
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    let image = new Image();
    image.src = reader.result;
    image.onload = function() {
      char_buttons.style.display = "none";
      img_btn_div.style.display = "none";
      input.style.display = "none";
      
      // Creating canvas to display
      canvasForHtml.style.display = "block";
      canvasForHtml.width = this.naturalWidth;
      canvasForHtml.height = this.naturalHeight;
      ctxForHtml.drawImage(this, 0, 0);
      
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
  const worker = await Tesseract.createWorker("Frak_LV_280721_500k", 1, {
    langPath: "https://artisozols.github.io/vd-jd/global"
  });
  
  const { data: { text } } = await worker.recognize(img);
  await worker.terminate();

  document.getElementById("loading").style.display = "none";
  output.style.backgroundColor = "white";
  output.style.opacity = "100%";
  output.value = convert_text(text);  
};

function convert_text(text) {
  py_convert_text = pyscript.interpreter.globals.get('convert');
  return py_convert_text(text);
};

function removeFiles() {
  input_btn.value = "";
  img_btn_div.style.display = "block";
  input.value = "";
  input.style.display = "block";
  input.focus();
  output.value = "";
  canvasForHtml.style.display = "none";
  char_buttons.style.display = "flex";
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
  const char_btn = char_buttons.children;
  for (let i = 0; i < char_btn.length; i++) {
    char_btn[i].style.backgroundColor = "transparent";
  }
};