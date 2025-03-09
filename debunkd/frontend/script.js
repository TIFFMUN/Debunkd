const textInput = document.getElementById("textInput");
const sampleTextBtn = document.getElementById("sampleTextBtn");
const uploadFileLabel = document.querySelector("label[for='imageUpload']");
const imageUpload = document.getElementById("imageUpload");
const checkButton = document.getElementById("processImage");

checkButton.style.display = "none";

function handleInputChange() {
    requestAnimationFrame(() => {
        if (textInput.value.trim() !== "" || imageUpload.files.length > 0) {
            sampleTextBtn.style.opacity = "0";  
            uploadFileLabel.style.opacity = "0";
            checkButton.style.display = "block";  
        } else {
            sampleTextBtn.style.opacity = "1";  
            uploadFileLabel.style.opacity = "1";
            checkButton.style.display = "none";
        }
    });
}

function insertSampleText() {
    textInput.value = "This is a sample text for misinformation detection.";
    handleInputChange();
}

async function extractTextFromImage(imageFile) {
    textInput.value = "Extracting text from image..."; // Show progress inside input field

    try {
        const { createWorker } = Tesseract;
        const worker = await createWorker();
        
        await worker.load();
        await worker.loadLanguage("eng");
        await worker.initialize("eng");

        const { data: { text } } = await worker.recognize(URL.createObjectURL(imageFile));
        await worker.terminate();

        return text.trim(); // Return extracted text
    } catch (error) {
        console.error("OCR Error:", error);
        textInput.value = "Error extracting text from image.";
        return ""; // Return empty string if OCR fails
    }
}

async function processCheck() {
    // Disable button & show "Processing..."
    checkButton.innerText = "Processing...";
    checkButton.disabled = true;

    let textToVerify = textInput.value.trim();

    // If no text is entered but an image is uploaded, extract text from image
    if (textToVerify === "" && imageUpload.files.length > 0) {
        textToVerify = await extractTextFromImage(imageUpload.files[0]);
        
        if (!textToVerify) {
            textInput.value = "No text detected in the image.";
            resetButton();
            return;
        }
    }

    // If still no text, show error
    if (textToVerify === "") {
        textInput.value = "Please enter text or upload an image.";
        resetButton();
        return;
    }

    try {
        // ✅ Send FormData (Correct format for Flask)
        let formData = new FormData();
        formData.append("text", textToVerify);

        const response = await fetch("http://127.0.0.1:5000/verify", {
            method: "POST",
            body: formData // Send as form-data to match Flask expectations
        });

        const data = await response.json();

        if (response.ok) {
            textInput.value = `Verification Result: ${data.result}`; // Show result inside input field
        } else {
            textInput.value = "Error verifying content.";
        }
    } catch (error) {
        console.error("Server Error:", error);
        textInput.value = "Error connecting to server.";
    }

    // ✅ Reset button after processing
    resetButton();
}

function resetButton() {
    checkButton.innerText = "Check"; 
    checkButton.disabled = false;
}

textInput.addEventListener("input", handleInputChange);
imageUpload.addEventListener("change", handleInputChange);
sampleTextBtn.addEventListener("click", insertSampleText);
checkButton.addEventListener("click", processCheck);

