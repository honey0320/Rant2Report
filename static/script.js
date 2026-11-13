const complaint = document.getElementById("complaint");
const count = document.getElementById("count");
const generateBtn = document.getElementById("generateBtn");
const statusBox = document.getElementById("status");
const results = document.getElementById("results");
let latestReport = null;

complaint.addEventListener("input", () => count.textContent = `${complaint.value.length} / 5000`);
document.getElementById("sampleBtn").addEventListener("click", () => {
  complaint.value = "The hostel Wi-Fi has not been working properly for the last 3 days. We have an exam tomorrow and students cannot access online notes or study materials. We have informed the hostel staff, but the issue is still not fixed.";
  count.textContent = `${complaint.value.length} / 5000`;
});

function reportText(r) {
  return `Subject: ${r.title}\n\nSummary:\n${r.summary}\n\nFormal Complaint:\n${r.description}\n\nRequested Action:\n${r.requested_action}`;
}

generateBtn.addEventListener("click", async () => {
  const text = complaint.value.trim();
  if (text.length < 12) {
    statusBox.textContent = "Please describe your complaint in a little more detail.";
    return;
  }
  generateBtn.disabled = true;
  generateBtn.innerHTML = "Understanding your complaint…";
  statusBox.textContent = "NLP is analysing the complaint, then Generative AI will write a new report.";
  results.classList.add("hidden");
  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({complaint: text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    latestReport = data.report;
    document.getElementById("category").textContent = data.analysis.category;
    document.getElementById("priority").textContent = data.analysis.priority;
    document.getElementById("duration").textContent = data.analysis.duration || "Not specified";
    document.getElementById("impact").textContent = data.analysis.impact.join(", ");
    document.getElementById("reportTitle").textContent = data.report.title;
    document.getElementById("summary").textContent = data.report.summary;
    document.getElementById("description").textContent = data.report.description;
    document.getElementById("requestedAction").textContent = data.report.requested_action;

    const missing = document.getElementById("missing");
    const missingWrap = document.getElementById("missingWrap");
    missing.innerHTML = "";
    if (data.report.missing_information && data.report.missing_information.length) {
      data.report.missing_information.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        missing.appendChild(li);
      });
      missingWrap.classList.remove("hidden");
    } else missingWrap.classList.add("hidden");

    const list = document.getElementById("destinationList");
    list.innerHTML = "";
    data.destinations.forEach(item => {
      const card = document.createElement("article");
      card.className = "destination";
      const title = document.createElement("h3");
      title.textContent = item.name;
      const desc = document.createElement("p");
      desc.textContent = item.description + (item.helpline ? " " + item.helpline : "");
      const link = document.createElement("a");
      link.href = item.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = "Visit official resource ↗";
      card.append(title, desc, link);
      list.appendChild(card);
    });
    results.classList.remove("hidden");
    statusBox.textContent = "Your report has been generated. Review it before using it.";
    results.scrollIntoView({behavior: "smooth", block: "start"});
  } catch (error) {
    statusBox.textContent = error.message;
  } finally {
    generateBtn.disabled = false;
    generateBtn.innerHTML = 'Understand & generate report <span>→</span>';
  }
});

document.getElementById("copyBtn").addEventListener("click", async () => {
  if (!latestReport) return;
  await navigator.clipboard.writeText(reportText(latestReport));
  statusBox.textContent = "Report copied to clipboard.";
});

document.getElementById("downloadBtn").addEventListener("click", () => {
  if (!latestReport) return;
  const blob = new Blob([reportText(latestReport)], {type: "text/plain;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Rant2Report.txt";
  a.click();
  URL.revokeObjectURL(url);
});
