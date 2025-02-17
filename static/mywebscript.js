function RunSentimentAnalysis() {
    let text = document.getElementById("textToAnalyze").value;

    if (!text) {
        document.getElementById("system_response").innerHTML = "Please enter text to analyze.";
        return;
    }

    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(text)}`)
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data); // ✅ Debugging: Log response in browser console

            if (data.error) {
                document.getElementById("system_response").innerHTML = `Error: ${data.error}`;
            } else {
                let dominantEmotion = data.dominant_emotion;
                let emotions = { ...data }; // Copy all emotions
                delete emotions.dominant_emotion; // Remove dominant emotion key from the list

                let emotionText = "For the given statement, the system response is:<br>";
                for (let [emotion, score] of Object.entries(emotions)) {
                    emotionText += `<b>'${emotion}': ${score.toFixed(6)}</b>, `;
                }

                emotionText = emotionText.slice(0, -2); // Remove the last comma and space
                emotionText += `<br>The dominant emotion is <b>${dominantEmotion}</b>.`;

                document.getElementById("system_response").innerHTML = emotionText;
            }
        })
        .catch(error => {
            document.getElementById("system_response").innerHTML = "An error occurred: " + error;
        });
}
