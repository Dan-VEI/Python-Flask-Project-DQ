import json
import requests

def emotion_detector(text_to_analyze):
    """
    Sends text to Watson API for emotion detection and returns the JSON response.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        # Make the API request
        response = requests.post(url, json=payload, headers=headers)

        # Raise an error for bad responses (e.g., 400, 500)
        response.raise_for_status()

        # Convert response to JSON
        response_json = response.json()

        # ✅ Debugging: Print/log the API response for inspection
        print("Watson API Response:", json.dumps(response_json, indent=2))

        return response_json  

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Watson API"}

def format_emotion_output(response_json):
    """
    Parses the JSON response from Watson, extracts emotion scores, and returns a dictionary.
    """
    try:
        # ✅ Check if response contains emotion predictions
        if "emotionPredictions" in response_json and response_json["emotionPredictions"]:
            emotion_data = response_json["emotionPredictions"][0].get("emotion", {})
        elif "emotion" in response_json:
            emotion_data = response_json["emotion"]
        else:
            print("Debugging: Unexpected API Response Format ->", response_json)
            return {"error": "No emotions found in response"}

        # ✅ Check if emotions are detected
        if not emotion_data:
            return {"error": "No emotions detected"}

        # ✅ Sort emotions by score in descending order
        sorted_emotions = sorted(emotion_data.items(), key=lambda item: item[1], reverse=True)

        # ✅ Build a sorted dictionary of emotions
        sorted_emotion_dict = {emotion: score for emotion, score in sorted_emotions}

        # ✅ Get the dominant (highest-scoring) emotion
        sorted_emotion_dict['dominant_emotion'] = sorted_emotions[0][0]

        return sorted_emotion_dict

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# ✅ Test the functions (run this script independently for debugging)
if __name__ == "__main__":
    test_text = "I love this new technology!"
    
    print("Sending test text to Watson API...")
    response = emotion_detector(test_text)

    print("Formatting the response...")
    formatted_output = format_emotion_output(response)

    print("Final Output:")
    print(json.dumps(formatted_output, indent=2))
