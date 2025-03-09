const textInput = document.getElementById("textInput");
const sampleTextBtn = document.getElementById("sampleTextBtn");
const uploadFileLabel = document.querySelector("label[for='imageUpload']");
const imageUpload = document.getElementById("imageUpload");
const checkButton = document.getElementById("processImage");
const clearButton = document.getElementById("clearButton");

let extractedText = ""; // Store OCR result separately

// Initially hide both Check and Clear buttons
checkButton.style.display = "none";
clearButton.style.display = "none";

function handleInputChange() {
    requestAnimationFrame(() => {
        if (textInput.value.trim() !== "" || imageUpload.files.length > 0) {
            sampleTextBtn.style.opacity = "0";  
            uploadFileLabel.style.opacity = "0";
            checkButton.style.display = "block";  
            clearButton.style.display = "block";  // Show Clear button as well
        } else {
            sampleTextBtn.style.opacity = "1";  
            uploadFileLabel.style.opacity = "1";
            checkButton.style.display = "none";
            clearButton.style.display = "none";  // Hide Clear button if no input
        }
    });
}

function insertSampleText() {
    textInput.value = "This is a sample text for misinformation detection.";
    extractedText = textInput.value; // Store it separately
    handleInputChange();
}

// ✅ When image is uploaded, update text box without passing it to OCR
imageUpload.addEventListener("change", async function () {
    if (imageUpload.files.length > 0) {
        textInput.value = "Image uploaded. Processing text...";
        extractedText = ""; // Reset extracted text
        handleInputChange();

        // Run OCR in background
        extractedText = await extractTextFromImage(imageUpload.files[0]);

        // Only update textInput if OCR found something
        if (extractedText) {
            textInput.value = extractedText;
        } else {
            textInput.value = "No text detected in the image.";
        }
    }
});

async function extractTextFromImage(imageFile) {
    try {
        const { createWorker } = Tesseract;
        const worker = await createWorker();
        
        await worker.load();
        await worker.loadLanguage("eng");
        await worker.initialize("eng");

        const { data: { text } } = await worker.recognize(URL.createObjectURL(imageFile));
        await worker.terminate();

        return text.trim(); // Store extracted text
    } catch (error) {
        console.error("OCR Error:", error);
        return ""; // Return empty string if OCR fails
    }
}

async function processCheck() {
    // Disable button & show "Processing..."
    checkButton.innerText = "Processing...";
    checkButton.disabled = true;

    let textToVerify = extractedText.trim() || textInput.value.trim(); // Use OCR result if available

    // If still no text, show error
    if (textToVerify === "" && imageUpload.files.length === 0) {
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

// Clear button function
function clearInput() {
    textInput.value = "";
    extractedText = ""; // Reset stored OCR text
    imageUpload.value = ""; // Reset file input
    checkButton.style.display = "none"; // Hide Check button
    clearButton.style.display = "none"; // Hide Clear button
    sampleTextBtn.style.opacity = "1";  
    uploadFileLabel.style.opacity = "1";
}

// Event Listeners
clearButton.addEventListener("click", clearInput);
textInput.addEventListener("input", handleInputChange);
imageUpload.addEventListener("change", handleInputChange);
sampleTextBtn.addEventListener("click", insertSampleText);
checkButton.addEventListener("click", processCheck);
