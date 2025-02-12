import unittest
from EmotionDetection.emotion_detection import emotion_detector, format_emotion_output
import json

class TestEmotionDetector(unittest.TestCase):
    def test_emotion_detector(self):
        test_cases = [
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear")
        ]

        for text, expected_emotion in test_cases:
          #  print(f"\nTesting input: {text}")

            # Get raw API response
            result_raw = emotion_detector(text)
          #  print("Raw API Response:", result_raw)  # Debugging step

            # Parse JSON response correctly
            result = format_emotion_output(result_raw)
          #  print("Formatted Output:", result)  # Debugging step

            # Check if 'dominant_emotion' exists before asserting
            if 'dominant_emotion' in result:
                self.assertEqual(result['dominant_emotion'], expected_emotion)
            else:
                self.fail(f"'dominant_emotion' key not found in formatted output for input: {text}")

if __name__ == '__main__':
    unittest.main()
