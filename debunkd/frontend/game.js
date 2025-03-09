

import { supabase } from './supabase.js';

let currentQuestionIndex = 0;
let questions = [];
let score = 0;
let highScore = 0;

async function loadQuestions() {
    const { data, error } = await supabase.from('questions').select('*');
    if (error) {
        console.error('Error fetching questions:', error);
        return;
    }
    questions = shuffleArray(data);
    preLoadFirstQuestion();
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function preLoadFirstQuestion() {
    if (questions.length > 0) {
        const quizContainer = document.querySelector(".quiz-container");
        quizContainer.style.backgroundImage = `url('${questions[0].image_url || "https://via.placeholder.com/600"}')`;
    }
    displayQuestion();
}

function displayQuestion() {
    const questionText = document.getElementById("question-text");
    const buttonContainer = document.querySelector(".button-container");
    const quizContainer = document.querySelector(".quiz-container");
    
    if (currentQuestionIndex >= 10 || currentQuestionIndex >= questions.length) {
        questionText.innerText = "Game Over!";
        buttonContainer.innerHTML = '<button onclick="restartGame()">Play Again</button>';
        return;
    }
    
    const q = questions[currentQuestionIndex];
    questionText.innerText = q.question;
    
    if (currentQuestionIndex > 0) {
        quizContainer.style.backgroundImage = `url('${q.image_url || "https://via.placeholder.com/600"}')`;
        quizContainer.style.transition = "background-image 0.5s ease-in-out";
    }
    
    buttonContainer.innerHTML = '<button onclick="checkAnswer(true)" class="btn">REAL</button> <button onclick="checkAnswer(false)" class="btn">FAKE</button>';
}

window.checkAnswer = function(userAnswer) {
    if (currentQuestionIndex >= 10) return;
    
    const correct = questions[currentQuestionIndex].answer;
    if (userAnswer === correct) {
        score++;
        document.getElementById("score").innerText = score;
    }
    
    if (score > highScore) {
        highScore = score;
        document.getElementById("high-score").innerText = highScore;
    }
    
    console.log(userAnswer === correct ? "✅ Correct!" : "❌ Wrong!");
    currentQuestionIndex++;
    displayQuestion();
};

window.restartGame = function() {
    currentQuestionIndex = 0;
    score = 0;
    document.getElementById("score").innerText = score;
    loadQuestions();
};

window.onload = loadQuestions;
