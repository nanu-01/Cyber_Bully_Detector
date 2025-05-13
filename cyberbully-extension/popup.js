document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("checkButton").addEventListener("click", async () => {
        const text = document.getElementById("textInput").value.trim();

        if (!text) {
            document.getElementById("result").innerText = "Please enter some text!";
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (data.TOXICITY && data.TOXICITY.summaryScore) {
                const score = data.TOXICITY.summaryScore.value;
                let resultText = `Toxicity Score: ${(score * 100).toFixed(1)}%`;

                if (score > 0.7) {
                    resultText += " 🚨 This might be cyberbullying!";
                    document.getElementById("result").classList.add("alert");
                } else {
                    document.getElementById("result").classList.remove("alert");
                }

                document.getElementById("result").innerText = resultText;
            } else {
                document.getElementById("result").innerText = "Could not analyze the text.";
            }
        } catch (error) {
            console.error("Error calling backend:", error);
            document.getElementById("result").innerText = "Error contacting backend.";
        }
    });
});
