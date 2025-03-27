from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import nltk
from disaster import load_model, predict_image, class_labels, severity_labels
from resource import allocate_resources
import torch
import os
from geotext import GeoText  # Module for detecting cities in text

# 🔹 Preprocessing for Tweet Classification
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# 🔹 Initialize Flask App
app = Flask(__name__)
CORS(app)

# 🔹 Load Tweet Classification Model & Vectorizer
model_filename = r"C:\Users\admin\Desktop\MiniProject\Project\project\models\tweet_classyfying_pa_bigram_model_2.pkl"
vectorizer_filename = r"C:\Users\admin\Desktop\MiniProject\Project\project\models\tfidf_vectorizer_bigram_2.pkl"

try:
    tweet_model = joblib.load(model_filename)
    tfidf_vectorizer = joblib.load(vectorizer_filename)
    print("✅ Tweet Classification Model & Vectorizer Loaded")
except Exception as e:
    print(f"❌ Error loading tweet model/vectorizer: {e}")

# 🔹 Load Image Classification Model
image_model_path = r"C:\Users\admin\Desktop\MiniProject\Project\project\models\chk_model.pth"
image_model, device = load_model(image_model_path)
print("✅ Image Classification Model Loaded")

lemma = nltk.WordNetLemmatizer()
stop = set(nltk.corpus.stopwords.words("english"))

# Base directory for disaster images
BASE_IMAGE_DIR = r"C:\Users\admin\Desktop\MiniProject\DisasterPro\project\Disaster_images"

def cleanTweet(txt):
    txt = txt.lower()
    words = nltk.word_tokenize(txt)
    words = [lemma.lemmatize(word) for word in words if word not in stop]
    return " ".join(words)

def extract_location(tweet):
    """Extracts the first city found in a tweet using GeoText."""
    places = GeoText(tweet)
    cities = places.cities  # Extracted city names
    return cities[0] if cities else None

# 🟢 **Route for Tweet Classification**
@app.route("/analyze-tweet", methods=["POST"])
def analyze_tweet():
    try:
        data = request.get_json()
        tweet = data.get("tweet", "")

        if not tweet:
            return jsonify({"error": "No tweet text provided"}), 400

        cleaned_tweet = cleanTweet(tweet)
        tfidf_tweet = tfidf_vectorizer.transform([cleaned_tweet])
        prediction = tweet_model.predict(tfidf_tweet)[0]

        # Extract location from tweet
        detected_city = extract_location(tweet)
        return jsonify({
            "result": "true" if prediction == 1 else "false",
            "location": detected_city if prediction == 1 else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🟢 **Route to Get Image List from Directory**
@app.route("/get-images", methods=["POST"])
def get_images():
    try:
        data = request.get_json()
        city_name = data.get("city")

        # Determine correct directory
        image_dir = os.path.join(BASE_IMAGE_DIR, city_name) if city_name else BASE_IMAGE_DIR
        if not os.path.exists(image_dir):
            return jsonify({"error": f"Image directory '{city_name}' not found"}), 404

        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        image_paths = [os.path.join(image_dir, img) for img in image_files]

        return jsonify({"images": image_paths})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🟢 **Route for Image Classification**
@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    try:
        if "image" in request.files:
            image = request.files["image"]
            return jsonify({"error": "Image file upload not supported. Use image path."}), 400

        elif request.is_json:
            data = request.get_json()
            image_path = data.get("image_path")

            if not image_path or not os.path.exists(image_path):
                return jsonify({"error": "Invalid or missing image path"}), 400

            # 🔹 Classify the image
            prediction = predict_image(image_model, image_path, device, class_labels, severity_labels)

            # 🔹 Allocate resources based on prediction
            allocate_resources(image_path)

            return jsonify(prediction)
        else:
            return jsonify({"error": "No image provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
