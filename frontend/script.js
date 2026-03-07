const API_URL = "https://startup-validator-api.onrender.com/analyze";

let currentReport = null;

async function analyzeIdea() {

    const ideaInput = document.getElementById("idea").value.trim();
    const loading = document.getElementById("loading");
    const report = document.getElementById("report");
    const downloadBtn = document.getElementById("downloadBtn");

    if (ideaInput === "") {
        alert("Please enter a startup idea first.");
        return;
    }

    report.innerHTML = "";
    downloadBtn.style.display = "none";
    loading.style.display = "block";

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ idea: ideaInput })
        });

        const data = await response.json();
        console.log(data);

        loading.style.display = "none";

        if (!data.ai_analysis) {
            report.innerHTML = `<p style="color:red;">Invalid response from server.</p>`;
            return;
        }

        currentReport = data;
        const analysis = data.ai_analysis;

        const similar = analysis.similar_startups || [];
        const suggestions = analysis.suggestions || [];

        const marketPotential =
            analysis.idea_scores && analysis.idea_scores.market_potential
                ? analysis.idea_scores.market_potential
                : "N/A";

        const competitionLevel =
            analysis.idea_scores && analysis.idea_scores.competition_level
                ? analysis.idea_scores.competition_level
                : "N/A";
        report.innerHTML = `

        <h2 class="report-title">Startup Analysis Report</h2>

        <div class="report-section">
            <h3>Startup Idea</h3>
            <p>${data.startup_idea || ideaInput}</p>
        </div>

        <div class="report-section">
            <h3>Category</h3>
            <p>${analysis.category || "Not available"}</p>
        </div>

        <div class="report-section">
            <h3>Viability Score</h3>
            <p>${analysis.viability_score || "N/A"} / 100</p>
        </div>

        <div class="report-section">
            <h3>Difficulty</h3>
            <p>${analysis.difficulty || "N/A"}</p>
        </div>

        <div class="report-section">
            <h3>Market Potential</h3>
            <p>${marketPotential} / 10</p>
        </div>

        <div class="report-section">
            <h3>Competition Level</h3>
            <p>${competitionLevel} / 10</p>
        </div>

        <div class="report-section">
            <h3>Similar Startups</h3>
            <ul>
                ${similar.map(s => `<li>${s}</li>`).join("")}
            </ul>
        </div>

        <div class="report-section">
            <h3>Suggestions</h3>
            <ul>
                ${suggestions.map(s => `<li>${s}</li>`).join("")}
            </ul>
        </div>

        `;

        downloadBtn.style.display = "inline-block";

    } catch (error) {

        loading.style.display = "none";

        report.innerHTML = `
        <p style="color:red;">
        Error connecting to AI service. Please try again later.
        </p>
        `;

        console.error(error);
    }
}



function downloadPDF() {

    if (!currentReport) {
        alert("No report available to download.");
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const analysis = currentReport.ai_analysis;

    const marketPotential = analysis.idea_scores?.market_potential || "N/A";

    const competitionLevel = analysis.idea_scores?.competition_level || "N/A";

    doc.setFontSize(18);
    doc.text("AI Startup Idea Analysis Report", 20, 20);

    doc.setFontSize(12);

    doc.text("Startup Idea: " + (currentReport.startup_idea || "N/A"), 20, 40);

    doc.text("Category: " + (analysis.category || "N/A"), 20, 50);

    doc.text("Viability Score: " + (analysis.viability_score || "N/A"), 20, 60);

    doc.text("Difficulty: " + (analysis.difficulty || "N/A"), 20, 70);

    doc.text("Market Potential: " + marketPotential + " / 10", 20, 80);

    doc.text("Competition Level: " + competitionLevel + " / 10", 20, 90);

    let y = 110;

    doc.text("Similar Startups:", 20, y);
    y += 10;

    (analysis.similar_startups || []).forEach(startup => {
        doc.text("- " + startup, 25, y);
        y += 8;
    });

    y += 10;

    doc.text("Suggestions:", 20, y);
    y += 10;

    (analysis.suggestions || []).forEach(s => {
        doc.text("- " + s, 25, y);
        y += 8;
    });

    doc.save("startup_analysis_report.pdf");
}