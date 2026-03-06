// API endpoint
const API_URL = "https://startup-validator-api.onrender.com/analyze";

let currentReport = null;


// Analyze Idea Function
async function analyzeIdea() {

    const ideaInput = document.getElementById("idea").value.trim();
    const loading = document.getElementById("loading");
    const report = document.getElementById("report");
    const errorBox = document.getElementById("errorBox");
    const downloadBtn = document.getElementById("downloadBtn");

    // Reset UI
    report.style.display = "none";
    downloadBtn.style.display = "none";
    errorBox.style.display = "none";

    if (ideaInput === "") {
        errorBox.innerText = "Please enter a startup idea.";
        errorBox.style.display = "block";
        return;
    }

    loading.style.display = "block";

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                idea: ideaInput
            })
        });

        const data = await response.json();

        loading.style.display = "none";

        if (!data.ai_analysis) {
            throw new Error("Invalid response from API");
        }

        currentReport = data;

        const analysis = data.ai_analysis;

        report.innerHTML = `
        
        <div class="report-section">
            <h3>Category</h3>
            <p>${analysis.category || "Not available"}</p>
        </div>

        <div class="report-section">
            <h3>Viability Score</h3>
            <p>${analysis.viability_score || "Not available"}</p>
        </div>

        <div class="report-section">
            <h3>Difficulty</h3>
            <p>${analysis.difficulty || "Not available"}</p>
        </div>

        <div class="report-section">
            <h3>Similar Startups</h3>
            <p>${(analysis.similar_startups || []).join(", ")}</p>
        </div>

        <div class="report-section">
            <h3>Suggestions</h3>
            <p>${(analysis.suggestions || []).join("<br>")}</p>
        </div>

        `;

        report.style.display = "block";
        downloadBtn.style.display = "inline-block";

    } catch (error) {

        loading.style.display = "none";

        errorBox.innerText = "Error connecting to AI service. Please try again.";
        errorBox.style.display = "block";

        console.error(error);
    }
}



// Dark Mode Toggle
function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

    const btn = document.querySelector(".theme-toggle");

    if (document.body.classList.contains("dark-mode")) {
        btn.innerHTML = "☀️ Light Mode";
    } else {
        btn.innerHTML = "🌙 Dark Mode";
    }
}



// Download PDF Report
function downloadPDF() {

    if (!currentReport) {
        alert("No report available to download.");
        return;
    }

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    const analysis = currentReport.ai_analysis;

    doc.setFontSize(18);
    doc.text("AI Startup Idea Analysis Report", 20, 20);

    doc.setFontSize(12);

    doc.text("Category: " + (analysis.category || "N/A"), 20, 40);

    doc.text("Viability Score: " + (analysis.viability_score || "N/A"), 20, 50);

    doc.text("Difficulty: " + (analysis.difficulty || "N/A"), 20, 60);

    doc.text("Similar Startups:", 20, 80);

    let y = 90;

    (analysis.similar_startups || []).forEach(startup => {
        doc.text("- " + startup, 25, y);
        y += 10;
    });

    y += 10;

    doc.text("Suggestions:", 20, y);

    y += 10;

    (analysis.suggestions || []).forEach(s => {
        doc.text("- " + s, 25, y);
        y += 10;
    });

    doc.save("startup_analysis_report.pdf");
}