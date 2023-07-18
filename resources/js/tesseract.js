const image_input = document.querySelector("#image_input");
const image_div = document.querySelector("#display_image")
const input = document.getElementById('input');
const output = document.getElementById('output');

image_input.addEventListener("change", function(){
  document.querySelector("#loading").style.display = "block";
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_img = reader.result;
    image_div.style.backgroundImage = `url(${uploaded_img})`;
    
    let image = new Image();
    image.src = reader.result;
    image.onload = function() {
      image_div.style.maxHeight = image.height + "px";
    };
    
    process_img = pyscript.interpreter.globals.get('process_img');
    let processed_img = process_img(uploaded_img);
    image_to_text(processed_img);
  });
  reader.readAsDataURL(this.files[0]);
});

async function image_to_text(img) {
  const worker = await Tesseract.createWorker({
    langPath: 'global',
    gzip: false,
    logger: m => console.log(m)
  });
  await worker.load();
  await worker.loadLanguage('Frak_LV_280721_500k');
  await worker.initialize('Frak_LV_280721_500k');
  const { data: { text } } = await worker.recognize(img);
  document.querySelector("#loading").style.display = "none";
  output.value = convert_text(text);
  await worker.terminate();
};

function removeFiles() {
  image_input.value = "";
  input.value = "";
  output.value = "";
  image_div.style.background = "none";
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