async function translateText() {
    const inputText = document.getElementById("inputText").value.trim();
    const sourceLang = document.getElementById("sourceLang").value;
    const targetLang = document.getElementById("targetLang").value;
    const outputTextArea = document.getElementById("outputText");

    if (!inputText) {
        outputTextArea.value = "";
        alert("Please enter text to translate!");
        return;
    }

    outputTextArea.value = "Translating...";

    // Switching to a robust, open-source Google Translate wrapper (Lingva API)
    const apiUrl = `https://lingva.ml/api/v1/${sourceLang}/${targetLang}/${encodeURIComponent(inputText)}`;

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Translation request failed");
        
        const data = await response.json();
        
        if (data && data.translation) {
            outputTextArea.value = data.translation;
        } else {
            outputTextArea.value = "Translation error. Try again.";
        }
    } catch (error) {
        console.error("Error executing translation lookup:", error);
        
        // Fallback option using an alternative public server if the main one is busy
        try {
            const fallbackUrl = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLang}&tl=${targetLang}&dt=t&q=${encodeURIComponent(inputText)}`;
            const fbResponse = await fetch(fallbackUrl);
            const fbData = await fbResponse.json();
            if (fbData && fbData[0] && fbData[0][0]) {
                outputTextArea.value = fbData[0].map(x => x[0]).join('');
            } else {
                outputTextArea.value = "Failed to translate.";
            }
        } catch (fallbackError) {
            outputTextArea.value = "Failed to connect to the translation server.";
        }
    }
}

// Clipboard copying functionality
function copyTranslation() {
    const outputText = document.getElementById("outputText");
    
    if (outputText.value && !outputText.value.startsWith("Translating") && !outputText.value.startsWith("Failed")) {
        navigator.clipboard.writeText(outputText.value)
            .then(() => {
                alert("Translation copied to clipboard! 👍");
            })
            .catch(err => {
                console.error("Could not copy text: ", err);
            });
    }
}

// Text-to-Speech Engine functionality
function speakTranslation() {
    const outputText = document.getElementById("outputText").value;
    const targetLang = document.getElementById("targetLang").value;

    if (outputText && !outputText.startsWith("Translating")) {
        window.speechSynthesis.cancel(); // Stop any previous ongoing speech

        const utterance = new SpeechSynthesisUtterance(outputText);
        
        const langMap = {
            "hi": "hi-IN",
            "en": "en-US",
            "fr": "fr-FR",
            "es": "es-ES",
            "de": "de-DE"
        };

        utterance.lang = langMap[targetLang] || "en-US";
        window.speechSynthesis.speak(utterance);
    }
}