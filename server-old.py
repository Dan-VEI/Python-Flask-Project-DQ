from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector, format_emotion_output

app = Flask(__name__)  # Initiate Flask

@app.route("/")
def render_index_page():
    return render_template("index.html")  # Main page

@app.route("/emotionDetector", methods=["POST"])
def emotion_detector_api():
    text_to_analyze = request.form.get("text")  # Get input text from form

    if not text_to_analyze:
        return jsonify({"error": "No text provided"}), 400

    # Get the raw API response and format it
    raw_response = emotion_detector(text_to_analyze)
    formatted_output = format_emotion_output(raw_response)

    # If no emotions were detected
    if not formatted_output:
        return jsonify({"error": "Could not analyze emotions"}), 500

    return jsonify(formatted_output)  # Return JSON response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)  # Only need this once
