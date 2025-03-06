// function analyzeImage() {
//     let imageInput = document.getElementById("imageUpload");

//     if (imageInput.files.length === 0) {
//         alert("Please upload an image first!");
//         return;
//     }

//     // Simulating an API request (Replace this with actual backend call)
//     document.getElementById("result").innerText = "Analyzing... Please wait.";

//     setTimeout(() => {
//         document.getElementById("result").innerText = "This image appears to be real.";
//     }, 2000);
// }

// Include Tesseract.js
const { createWorker } = Tesseract;

// Initialize the Tesseract worker
async function initWorker() {
    const worker = await createWorker();
    await worker.load();
    await worker.loadLanguage("eng");
    await worker.initialize("eng");
    return worker;
}

document.getElementById("processImage").addEventListener("click", async () => {
    const fileInput = document.getElementById("imageUpload");
    const outputElement = document.getElementById("output");

    // Show processing message while working
    outputElement.innerText = "Processing...";

    // Check if a file is selected
    if (fileInput.files.length === 0) {
        outputElement.innerText = "Please upload an image first.";
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = async function () {
        try {
            // Initialize worker
            const worker = await initWorker();

            // Recognize text from the uploaded image
            const { data: { text } } = await worker.recognize(reader.result);
            await worker.terminate(); // Terminate the worker once done

            // Keep "Processing..." for a short while before displaying the result
            setTimeout(async () => {
                // Send extracted text to backend for verification
                const verificationResult = await verifyStatement(text);
                outputElement.innerText = `Verification Result: ${verificationResult}`;
            }, 1500); // Delay of 1.5 seconds before replacing the text
        } catch (error) {
            console.error("Error processing image:", error);
            outputElement.innerText = "An error occurred while processing the image.";
        }
    };

    // Read the image file as a data URL
    reader.readAsDataURL(file);
});

// Function to send extracted text to the backend
async function verifyStatement(statement) {
    try {
        const response = await fetch("http://127.0.0.1:5000/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ statement }),
        });

        const data = await response.json();

        if (response.ok) {
            return data.result; // Return the verification result
        } else {
            console.error("Backend Error:", data.error);
            return "Error verifying statement.";
        }
    } catch (error) {
        console.error("Error verifying statement:", error);
        return "Error verifying statement.";
    }
}