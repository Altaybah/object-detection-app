#import the required libraries
import os                                            
from flask import Flask, request, render_template    # Flask the app, the user's data, sends the HTML page back
from ultralytics import YOLO     # loads best.pt -trained model from google colab from previous challenge- and runs detection
from PIL import Image            # used to shrink large images

app = Flask(__name__)                               

# --------------------------------------------------------------
# The model is loaded only when the first user uploads an image,this makes the app start fast on the free render server
model = None

def get_model():
    global model
    if model is None:                               
        model = YOLO("best.pt")                      
    return model

# -----------------------------------------------------------
# Uploaded photos and result images are stored in static < results
RESULTS_FOLDER = os.path.join("static", "results")
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# -----------------------------------------------------
# GET show the empty upload page ... POST the uaer upload image - run detection and show the result

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["image"]               

        if not file.filename.lower().endswith((".jpg", ".jpeg")):    # accept JPG only and show a error if any other type used
            return render_template("index.html", result_image=None,
                                   error="Please upload a JPG image only.")

       
        image_path = os.path.join(RESULTS_FOLDER, file.filename)   # save the original upload
        file.save(image_path)

        #shrink large photos max 640px - so the small free server can handle them
        img = Image.open(image_path)
        img.thumbnail((640, 640))
        img.save(image_path)

        #run detection
        results = get_model().predict(image_path, conf=0.3, imgsz=416,
                                      device="cpu", verbose=False)

        #save a copy of the image with the boxes drawn on it
        result_path = os.path.join(RESULTS_FOLDER, "result_" + file.filename)
        results[0].save(filename=result_path)

        #send the page back with the result image
        return render_template("index.html", result_image=result_path)

    return render_template("index.html", result_image=None)

# -----------------------------------------------------
# Start the web server
app.run(host="0.0.0.0", port=5000, debug=False)
