const image_input = document.querySelector("#image_input");
var uploaded_image = "";

image_input.addEventListener("change", function(){
  document.querySelector("#message").style.display = "block";
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    uploaded_image = reader.result;
    document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`;
    image_to_text(uploaded_image);
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

  py_convert_text = pyscript.interpreter.globals.get('convert')
  const new_text = py_convert_text(text)

  document.getElementById('message').innerHTML = new_text;
  await worker.terminate();
};
