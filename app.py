import os
from flask import Flask, request, render_template
from ultralytics import YOLO

app = Flask(__name__)

# Load the model ONCE when the server starts (not on every request!)
model = YOLO("best.pt")

# Folder where result images will be saved
RESULTS_FOLDER = os.path.join("static", "results")
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # 1. Get the uploaded file from the form
        file = request.files["image"]

        # 2. Only accept JPG images
        if not file.filename.lower().endswith((".jpg", ".jpeg")):
            return render_template("index.html", result_image=None,
                                   error="Please upload a JPG image only.")

        # 3. Save it into static/results
        image_path = os.path.join(RESULTS_FOLDER, file.filename)
        file.save(image_path)

        # 4. Run the model on it
        results = model.predict(image_path, conf=0.3)

        # 5. Save the image with boxes drawn
        result_path = os.path.join(RESULTS_FOLDER, "result_" + file.filename)
        results[0].save(filename=result_path)

        # 6. Show the page again with the result
        return render_template("index.html", result_image=result_path)

    # First visit (GET): just show the empty page
    return render_template("index.html", result_image=None)

app.run(host="0.0.0.0", port=5000, debug=True)