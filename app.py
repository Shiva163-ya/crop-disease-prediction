from flask import Flask, render_template, request
from PIL import Image
import numpy as np

app = Flask(__name__)


def classify_leaf(image_array):
    img = image_array
    r = img[:, :, 0].mean()
    g = img[:, :, 1].mean()
    b = img[:, :, 2].mean()

    green_ratio = np.mean(img[:, :, 1] > 100)
    red_ratio = np.mean(img[:, :, 0] > 150)
    brightness = (r + g + b) / 3

    if green_ratio > 0.55 and brightness > 110:
        return "Healthy Leaf", "The crop appears healthy and has a strong green color."
    if red_ratio > 0.22 and green_ratio < 0.6:
        return "Rust Disease", "Red/brown discoloration suggests rust disease. Use fungicide and remove infected leaves."
    if green_ratio < 0.5:
        return "Blight / Leaf Spot", "The leaf shows signs of blight or fungal spotting. Improve airflow and avoid excess moisture."
    return "Leaf Spot Suspected", "The image shows discoloration that may indicate early fungal stress. Monitor the plant closely."


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        file = request.files.get("leaf_image")
        if file and file.filename:
            try:
                img = Image.open(file).convert("RGB")
                arr = np.array(img)
                prediction = classify_leaf(arr)
            except Exception:
                prediction = ("Invalid image", "Please upload a valid image file.")
    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
