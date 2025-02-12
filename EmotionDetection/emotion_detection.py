import json
import requests

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def format_emotion_output(response_text):
    """
    Parses the JSON response from Watsonx, extracts the emotion scores, sorts them
    in descending order, and returns a dictionary of emotions and their scores.
    """
    data = json.loads(response_text)    # Convert JSON string to Python dictionary
    
    # Extract the emotion scores from Watsonx's output structure.
    if "emotionPredictions" in data and len(data["emotionPredictions"]) > 0:
        emotion_data = data["emotionPredictions"][0].get("emotion", {})
    elif "emotion" in data:
        emotion_data = data["emotion"]
    else:
        emotion_data = data
    
    # Sort the emotions by score (value) in descending order.
    sorted_emotions = sorted(emotion_data.items(), key=lambda item: item[1], reverse=True)
    
    # Build and return a dictionary from the sorted tuples.
    sorted_emotion_dict = {emotion: score for emotion, score in sorted_emotions}
    return sorted_emotion_dict

if __name__ == "__main__":
    # Example text to analyze
    text = "I love this new technology!"
    
    # Get the raw response from the emotion detector API.
    response_text = emotion_detector(text)
    
    # Format the response into a sorted dictionary.
    emotion_dict = format_emotion_output(response_text)
    
    # Print the formatted output according to the specifications.
    print("{")
    # Print each emotion and its score on its own line, with keys in single quotes and a trailing comma.
    for emotion, score in emotion_dict.items():
        print(f"  '{emotion}': {score},")
    
    # Determine which emotion has the highest score.
    highest_emotion = max(emotion_dict, key=emotion_dict.get)
    # Print the dominant emotion line with single quotes around both the key and the value.
    print(f"  'dominant_emotion': '{highest_emotion}',")
    print("}")
