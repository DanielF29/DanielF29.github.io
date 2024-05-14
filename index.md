---
layout: default
title: Home
permalink: /
---

<div style="display: flex; align-items: flex-start;">
    <img src="/images/DFA_outframed.png" alt="Selfie" style="max-width: 25%; height: auto; margin-right: 20px;"/>
    <div>
        <h1>Welcome to My Personal Webpage</h1>

        <p>Welcome to my website! Here, you can learn more about me, see the projects I've worked on, and find out how to contact me.</p>

        <h2>Basic personal Info:</h2>

        <p>I am a Ph.D. candidate at Tecnológico de Monterrey, México. My research is on Explainable Artificial Intelligence (XAI) and Causality within the context of medical imaging. 
        My passion lies in leveraging my abilities to tackle intricate challenges, drive innovation, and make meaningful contributions to the technological domain.</p>

        <p>Additionally, I have a broad interest in deep learning news and its breakthroughs, gaming, new tech gadgets, and the exploration of space.</p>

        <h2>Basic Contact information:</h2>

        <p>Feel free to reach out to me via email at <span id="email">ing.daniel.bin@gmail.com</span> <button id="copyButton" onclick="copyEmail()">Copy Email</button> or check <a href="/contact">Contact</a>.</p>

        <p>[<a href="/about">About</a>] | [<a href="/projects">Projects</a>] | [<a href="/contact">Contact</a>] | [<a href="/publications">Publications</a>] | [<a href="/current_mentoring_project">Current Mentoring Project</a>]</p>
    </div>
</div>

<script>
function copyEmail() {
    var email = document.getElementById("email").innerText;
    navigator.clipboard.writeText(email).then(function() {
        alert("Email copied to clipboard!");
    }, function(err) {
        console.error("Could not copy text: ", err);
    });
}
</script>

<style>
    #copyButton {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.4s;
    }

    #copyButton:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
</style>