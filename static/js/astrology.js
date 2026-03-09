const astrologyResult = document.getElementById("astro-result");
const submitBtn = document.getElementById("astro-submit");
const previewBox = document.getElementById("astro-preview");

function renderMessage(type, html) {
    astrologyResult.className = `result-panel astro-result-panel ${type === "error" ? "result-error" : "result-success"}`;
    astrologyResult.innerHTML = html;
}

function isValidDateFormat(value) {
    return /^\d{4}-\d{2}-\d{2}$/.test(value);
}

function isValidTimeFormat(value) {
    return /^\d{2}:\d{2}$/.test(value);
}

function updatePreview() {
    const fullName = document.getElementById("astro-full-name").value.trim() || "(missing)";
    const gender = document.getElementById("astro-gender").value || "(missing)";
    const dateOfBirth = document.getElementById("astro-dob").value || "(missing)";
    const timeOfBirth = document.getElementById("astro-tob").value || "(missing)";
    const location = document.getElementById("astro-location").value.trim() || "(missing)";

    previewBox.innerHTML = `
        <div class="stat-item"><span class="stat-label">Full Name</span><span class="stat-value">${fullName}</span></div>
        <div class="stat-item"><span class="stat-label">Gender</span><span class="stat-value">${toTitleCase(gender)}</span></div>
        <div class="stat-item"><span class="stat-label">Date of Birth</span><span class="stat-value">${dateOfBirth}</span></div>
        <div class="stat-item"><span class="stat-label">Time of Birth</span><span class="stat-value">${timeOfBirth}</span></div>
        <div class="stat-item"><span class="stat-label">Location</span><span class="stat-value">${location}</span></div>
    `;
}

function toTitleCase(value) {
    if (!value) return "";
    return value.charAt(0).toUpperCase() + value.slice(1);
}

function renderAnalysisDetails(details) {
    if (!details) return "";

    const scoreRows = Object.entries(details.signal_scores || {})
        .map(([k, v]) => `<li><strong>${k}</strong>: ${v}</li>`)
        .join("");

    const factorRows = (details.matched_factors || [])
        .map((x) => `<li>${x}</li>`)
        .join("");

    const recRows = (details.selected_recommendations || [])
        .map((r) => `<li>#${r.rank} (score ${r.score}): ${r.message}</li>`)
        .join("");

    const topicRows = (details.decision_topics || [])
        .map((t) => `<li><strong>${t.label}</strong> (keyword: ${t.keyword}, intent: ${t.intent})</li>`)
        .join("");

    const ruleRows = (details.expert_rule_hits || [])
        .map((r) => `<li><strong>${r.id}</strong>: ${r.conclusion}</li>`)
        .join("");

    const followupRows = (details.follow_up_questions || [])
        .map((q) => `<li>${q}</li>`)
        .join("");

    const moduleRows = (details.libraries_and_modules || [])
        .map((x) => `<li>${x}</li>`)
        .join("");

    const kr = details.knowledge_representation || {};
    const symbolRows = (kr.symbol_tables || [])
        .map((x) => `<li>${x}</li>`)
        .join("");

    const stepRows = (details.pipeline_steps || [])
        .map((x) => `<li>${x}</li>`)
        .join("");

    const plan = details.symbolic_plan || {};
    const planRows = (plan.selected_plan_actions || [])
        .map((x) => `<li>${x}</li>`)
        .join("");
    const bfs = plan.uninformed_bfs || {};
    const astar = plan.informed_a_star || {};

    const external = details.external_api || {};
    const topResult = external.top_result || {};
    const disclosures = details.disclosures || {};
    const coords = external.coordinates
        ? `${external.coordinates.latitude}, ${external.coordinates.longitude}`
        : "Unavailable";

    return `
        <details style="margin-top: 16px;">
            <summary><strong>How This Conclusion Was Produced</strong></summary>
            <div style="margin-top: 12px;">
                <p><strong>Sign Source:</strong> ${details.sign_source}</p>
                <p><strong>Gender:</strong> ${toTitleCase(details.gender || "N/A")}</p>
                <p><strong>Gender Guidance Rule:</strong> ${details.gender_guidance || "Not applicable for this intent"}</p>
                <p><strong>Detected Intent:</strong> ${details.intent} (${details.confidence}% confidence)</p>
                <p><strong>External API Used:</strong> ${external.used ? "Yes" : "No"}</p>
                <p><strong>External Provider:</strong> ${external.provider || "N/A"}</p>
                <p><strong>External API Details:</strong> ${external.details || "N/A"}</p>
                <p><strong>API Query:</strong> ${external.query || "N/A"}</p>
                <p><strong>Request URL:</strong> ${external.request_url || "N/A"}</p>
                <p><strong>HTTP Status:</strong> ${external.http_status ?? "N/A"}</p>
                <p><strong>Duration:</strong> ${external.duration_ms ?? "N/A"} ms</p>
                <p><strong>Cached Result:</strong> ${external.cached ? "Yes" : "No"}</p>
                <p><strong>Coordinates:</strong> ${coords}</p>
                <p><strong>Top Geocode Result:</strong> ${topResult.display_name || "N/A"}</p>
                <p><strong>Top Result Type:</strong> ${topResult.type || "N/A"} (importance: ${topResult.importance ?? "N/A"})</p>
                <h4>Decision Topic Matches</h4>
                <ul>${topicRows || "<li>None</li>"}</ul>
                <h4>Signal Scores</h4>
                <ul>${scoreRows}</ul>
                <h4>Matched Factors</h4>
                <ul>${factorRows || "<li>None</li>"}</ul>
                <h4>Selected Recommendations</h4>
                <ul>${recRows}</ul>
                <h4>Expert Rule Matches</h4>
                <ul>${ruleRows || "<li>No rules triggered</li>"}</ul>
                <h4>Suggested Follow-up Questions</h4>
                <ul>${followupRows || "<li>No follow-up questions generated</li>"}</ul>
                <h4>Symbolic Plan (${plan.selected_method || "N/A"})</h4>
                <ul>${planRows || "<li>No plan generated</li>"}</ul>
                <p><strong>Search Stats:</strong> BFS expanded ${bfs.nodes_expanded ?? "N/A"} nodes, A* expanded ${astar.nodes_expanded ?? "N/A"} nodes.</p>
                <h4>Modules/Libraries Used</h4>
                <ul>${moduleRows}</ul>
                <h4>Knowledge Representation</h4>
                <p><strong>Planning Graph:</strong> ${kr.planning_graph_type || "N/A"}</p>
                <p><strong>Memory Store:</strong> ${kr.memory_store || "N/A"}</p>
                <ul>${symbolRows}</ul>
                <h4>Pipeline Steps</h4>
                <ol>${stepRows}</ol>
                <h4>Disclosures</h4>
                <p><strong>Main:</strong> ${disclosures.main_disclaimer || "N/A"}</p>
                <p><strong>Privacy:</strong> ${disclosures.data_privacy_notice || "N/A"}</p>
                <p><strong>Sources Note:</strong> ${disclosures.sources_note || "N/A"}</p>
            </div>
        </details>
    `;
}

async function analyzeAstrology() {
    const fullName = document.getElementById("astro-full-name").value.trim();
    const gender = document.getElementById("astro-gender").value.trim();
    const dateOfBirth = document.getElementById("astro-dob").value;
    const timeOfBirth = document.getElementById("astro-tob").value;
    const locationOfBirth = document.getElementById("astro-location").value.trim();
    const statement = document.getElementById("astro-statement").value.trim();
    const sign = document.getElementById("astro-sign").value;
    const sessionId = document.getElementById("astro-session").value.trim() || "default";

    if (!fullName) {
        renderMessage("error", "<strong>Error:</strong> Please enter full name.");
        return;
    }
    if (!gender) {
        renderMessage("error", "<strong>Error:</strong> Please choose gender.");
        return;
    }
    if (!dateOfBirth) {
        renderMessage("error", "<strong>Error:</strong> Please enter date of birth.");
        return;
    }
    if (!isValidDateFormat(dateOfBirth)) {
        renderMessage("error", "<strong>Error:</strong> Date must be in YYYY-MM-DD format.");
        return;
    }
    if (!timeOfBirth) {
        renderMessage("error", "<strong>Error:</strong> Please enter time of birth.");
        return;
    }
    if (!isValidTimeFormat(timeOfBirth)) {
        renderMessage("error", "<strong>Error:</strong> Time must be in HH:MM 24-hour format.");
        return;
    }
    if (!locationOfBirth) {
        renderMessage("error", "<strong>Error:</strong> Please enter location of birth.");
        return;
    }
    if (!statement) {
        renderMessage("error", "<strong>Error:</strong> Please enter a statement.");
        return;
    }

    renderMessage("success", "<span class='loading'></span> Analyzing your statement...");

    try {
        const response = await fetch("/api/astrology/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                full_name: fullName,
                gender: gender,
                date_of_birth: dateOfBirth,
                time_of_birth: timeOfBirth,
                location_of_birth: locationOfBirth,
                statement: statement,
                sign: sign,
                session_id: sessionId
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            renderMessage("error", `<strong>Error:</strong> ${data.error || "Analysis failed"}`);
            return;
        }

        const pretty = (data.response || "").replace(/\n/g, "<br>");
        const detailsHtml = renderAnalysisDetails(data.analysis_details);
        const confidence = data.analysis_details?.confidence || 0;
        const intent = toTitleCase(data.analysis_details?.intent || "general");
        const shortDisclaimer = data.analysis_details?.disclosures?.short_disclaimer || "";
        renderMessage(
            "success",
            `<div class="result-meta">
                <div class="meta-item"><strong>Sign</strong><br>${toTitleCase(data.sign)}</div>
                <div class="meta-item"><strong>Gender</strong><br>${toTitleCase(data.gender || "N/A")}</div>
                <div class="meta-item"><strong>Intent</strong><br>${intent}</div>
                <div class="meta-item"><strong>Sign Source</strong><br>${data.sign_source}</div>
                <div class="meta-item"><strong>Session</strong><br>${data.session_id}</div>
            </div>
            <div class="confidence-bar"><span style="width: ${confidence}%;"></span></div>
            <p style="margin-top: 8px;"><strong>Confidence:</strong> ${confidence}%</p>
             <div style="margin-top: 10px;">${pretty}</div>
             ${shortDisclaimer ? `<p style="margin-top: 10px;"><strong>Disclaimer:</strong> ${shortDisclaimer}</p>` : ""}
             ${detailsHtml}`
        );
    } catch (error) {
        renderMessage("error", "<strong>Error:</strong> Could not reach the astrology API.");
    }
}

submitBtn.addEventListener("click", analyzeAstrology);
document.getElementById("astro-full-name").addEventListener("input", updatePreview);
document.getElementById("astro-gender").addEventListener("change", updatePreview);
document.getElementById("astro-dob").addEventListener("input", updatePreview);
document.getElementById("astro-tob").addEventListener("input", updatePreview);
document.getElementById("astro-location").addEventListener("input", updatePreview);
updatePreview();

document.querySelectorAll(".quick-prompt").forEach((btn) => {
    btn.addEventListener("click", () => {
        const prompt = btn.getAttribute("data-prompt");
        document.getElementById("astro-statement").value = prompt;
    });
});
