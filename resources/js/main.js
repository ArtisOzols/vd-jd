const input_btn = document.getElementById("img_input_btn"); // input that takes image
const btn_div = document.getElementById("btn_div"); // button that sets value to input_btn
const input = document.getElementById('input');
const output = document.getElementById('output');
const char_buttons = document.getElementById('character_buttons');
const canvasForHtml = document.getElementById("img_canvas");
const ctxForHtml = canvasForHtml.getContext('2d');
const dropdown = document.getElementById("dropdown");
var convert_ee_r = {"ee": false, "r": true};

// Dropdown optoins
function unhideDropdown() {
  dropdown.style.display = (dropdown.style.display === 'none') ? 'block' : 'none';
};

document.addEventListener('click', function(event) {
  if (!event.target.matches('.overlay, #dropdown, #dropdown button, #dropdown button span')) {
    dropdown.style.display = 'none';
  };
});

function checkUncheck(id) {
  var x = document.getElementById("check_"+id);
  x.innerHTML = (x.innerHTML === "☐ ") ? "☒ " : "☐ ";
  convert_ee_r[id] = convert_ee_r[id] ? false : true;
  set_output_val();
};

// Upload image from input button
input_btn.addEventListener("change", function(){
  processImage(this.files[0]);
});

// Upload image from clipboard
document.onpaste = function(pasteEvent) {
  var item = pasteEvent.clipboardData.items[0];
  if (item.type.indexOf("image") === 0){
    var file = item.getAsFile();
    processImage(file);
  }
}

function processImage(file) {
  document.getElementById("loading").style.display = "block";
  output.style.backgroundColor = "lightgray";
  output.style.opacity = "20%";
  
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    let image = new Image();
    image.src = reader.result;
    image.onload = function() {
      char_buttons.style.display = "none";
      btn_div.style.display = "none";
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
  reader.readAsDataURL(file);
}


// Text recognition
async function image_to_text(img) {
  const worker = await Tesseract.createWorker("Frak_LV_280721_500k", 1, {
    langPath: "https://artisozols.github.io/vd-jd/global"
  });
  const { data: { text } } = await worker.recognize(img);
  await worker.terminate();

  document.getElementById("loading").style.display = "none";
  output.style.backgroundColor = "white";
  output.style.opacity = "100%";
  output.value = convert(text, convert_ee_r["r"], convert_ee_r["ee"]);
};

// Clear input/output
function clearAll() {
  input_btn.value = "";
  btn_div.style.display = "flex";
  input.value = "";
  input.style.display = "block";
  input.focus();
  output.value = "";
  canvasForHtml.style.display = "none";
  char_buttons.style.display = "flex";
};

// Converts text from input textarea 
function set_output_val() {
  output.value = convert(input.value, convert_ee_r["r"], convert_ee_r["ee"]);
};
input.addEventListener('input', set_output_val);
set_output_val();

// Adds old Latvian Characters
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