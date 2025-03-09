import { supabase } from './supabase.js';

let currentQuestionIndex = 0;
let questions = [];

async function loadQuestions() {
    const { data, error } = await supabase.from('questions').select('*');
    if (error) console.error('Error fetching questions:', error);
    else questions = data;
    displayQuestion();
}

function displayQuestion() {
    if (currentQuestionIndex >= questions.length) {
        document.getElementById("question-text").innerText = "Game Over!";
        return;
    }
    const q = questions[currentQuestionIndex];
    document.getElementById("question-text").innerText = q.question;
    document.getElementById("question-image").src = q.image_url || "https://via.placeholder.com/300";
}

window.checkAnswer = function(userAnswer) {
    const correct = questions[currentQuestionIndex].answer;
    alert(userAnswer === correct ? "✅ Correct!" : "❌ Wrong!");
    currentQuestionIndex++;
    displayQuestion();
};

window.onload = loadQuestions;

