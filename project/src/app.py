from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import nltk
from disaster import load_model, predict_image, class_labels, severity_labels
import torch

# 🔹 Preprocessing for Tweet Classification
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# 🔹 Initialize Flask App
app = Flask(__name__)
CORS(app)

# 🔹 Load Tweet Classification Model & Vectorizer
model_filename = r"project\models\tweet_classyfying_pa_bigram_model_2.pkl"
vectorizer_filename = r"project\models\tfidf_vectorizer_bigram_2.pkl"

try:
    tweet_model = joblib.load(model_filename)
    tfidf_vectorizer = joblib.load(vectorizer_filename)
    print("✅ Tweet Classification Model & Vectorizer Loaded")
except Exception as e:
    print(f"❌ Error loading tweet model/vectorizer: {e}")

# 🔹 Load Image Classification Model
image_model_path = r"C:\Users\admin\Desktop\MiniProject\DisasterPro\project\models\best_model.pth"
image_model, device = load_model(image_model_path)
print("✅ Image Classification Model Loaded")

lemma = nltk.WordNetLemmatizer()
stop = set(nltk.corpus.stopwords.words("english"))

def cleanTweet(txt):
    txt = txt.lower()
    words = nltk.word_tokenize(txt)
    words = [lemma.lemmatize(word) for word in words if word not in stop]
    return " ".join(words)

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

        return jsonify({"result": "true" if prediction == 1 else "false"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🟢 **Route for Image Classification**
@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    prediction = predict_image(image_model, image, device, class_labels, severity_labels)

    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)
