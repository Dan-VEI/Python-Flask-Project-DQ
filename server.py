from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector, format_emotion_output

app = Flask(__name__)  # Flask app initialization

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/emotionDetector", methods=['GET', 'POST'])
def sent_detector():
    text_to_analyze = request.args.get("textToAnalyze") or request.form.get("textToAnalyze")

    if not text_to_analyze:
        return jsonify({"error": "No text provided for analysis"}), 400  

    # Call Watson API
    response_json = emotion_detector(text_to_analyze)

    # ✅ Debugging: Print API response in Flask logs
    print("Raw Watson API Response:", response_json)

    # Check if Watson API returned an error
    if "error" in response_json:
        return jsonify(response_json), 500  

    # Process Watson API response
    formatted_response = format_emotion_output(response_json)

    # ✅ Debugging: Print formatted emotions in Flask logs
    print("Formatted Emotion Output:", formatted_response)

    # Check if the formatted response contains an error
    if "error" in formatted_response:
        return jsonify(formatted_response), 500  

    # ✅ Return the JSON result to the web page
    return jsonify(formatted_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
