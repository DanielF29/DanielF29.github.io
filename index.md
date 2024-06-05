---
layout: default
title: Digital_Daniel
permalink: /
---

<div style="display: flex; align-items: flex-start;">
    <img src="/images/DFA_outframed.png" alt="Selfie" style="max-width: 25%; height: auto; margin-right: 20px;"/>
    <div>
        <h1>Welcome, </h1>

        <p>Here, you can learn more about me, see the projects I've worked on, and find out how to contact me.</p>

        <h2>Basic personal Info:</h2>

        <p>I am a Ph.D. candidate at Tecnológico de Monterrey, México. My research is on Explainable Artificial Intelligence (XAI) and Causality within the context of medical imaging. 
        My passion lies in leveraging my abilities to tackle intricate challenges, drive innovation, and make meaningful contributions to the technological domain.</p>

        <p>Additionally, I have a broad interest in deep learning news and its breakthroughs, gaming, new tech gadgets, and the exploration of space.</p>

        <h2>Skills</h2>
        <ul>
            <li><strong>Programming Languages:</strong> Python (5+ years), R, C, C++, C#</li>
            <li><strong>Databases:</strong> MySQL, Postgres</li>
            <li><strong>Tools and IDEs:</strong> Git, Vim, Docker, Sklearn, Pandas, Pytorch, Matplotlib, Plotly, Visual Studio Code</li>
            <li><strong>Other Software:</strong> NetLogo, MATLAB, Solid Edge, MPLAB, EAGLE</li>
            <li><strong>Personal Skills:</strong> Critical-thinking, Collaborative, Problem-solving, Proactive, Oral and written communication</li>
        </ul>

        <h2>Basic Contact information:</h2>

        <p>Feel free to reach out to me via email at <span id="email">ing.daniel.bin@gmail.com</span> <button id="copyButton" onclick="copyEmail()">Copy Email</button> or check <a href="/contact">Contact</a>.</p>


        <p>
            <a href="/about" class="button">About</a> | 
            <a href="/projects" class="button">Projects</a> | 
            <a href="/contact" class="button">Contact</a> | 
            <a href="/publications" class="button">Publications</a> | 
            <a href="/current_mentoring_project" class="button">Current Mentoring Project</a>
        </p>
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
        color: black;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.2s;
    }

    #copyButton:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }

    .button {
        background-color: #ADD8E6; /* light blue */
        border: none;
        color: black;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.2s;
    }

    .button:hover {
        background-color: white;
        color: black;
        border: 2px solid #ADD8E6;
    }

</style>