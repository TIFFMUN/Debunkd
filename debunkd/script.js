function analyzeImage() {
    let imageInput = document.getElementById("imageUpload");

    if (imageInput.files.length === 0) {
        alert("Please upload an image first!");
        return;
    }

    // Simulating an API request (Replace this with actual backend call)
    document.getElementById("result").innerText = "Analyzing... Please wait.";

    setTimeout(() => {
        document.getElementById("result").innerText = "This image appears to be real.";
    }, 2000);
}
