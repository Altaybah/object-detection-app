import os
from flask import Flask, request, render_template
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)

model = YOLO("best.pt")

RESULTS_FOLDER = os.path.join("static", "results")
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["image"]

        if not file.filename.lower().endswith((".jpg", ".jpeg")):
            return render_template("index.html", result_image=None,
                                   error="Please upload a JPG image only.")

        image_path = os.path.join(RESULTS_FOLDER, file.filename)
        file.save(image_path)

        # Shrink large images to save memory on the small server
        img = Image.open(image_path)
        img.thumbnail((640, 640))
        img.save(image_path)

        results = model.predict(image_path, conf=0.3, imgsz=416, device="cpu", verbose=False)

        result_path = os.path.join(RESULTS_FOLDER, "result_" + file.filename)
        results[0].save(filename=result_path)

        return render_template("index.html", result_image=result_path)

    return render_template("index.html", result_image=None)

app.run(host="0.0.0.0", port=5000, debug=False)
