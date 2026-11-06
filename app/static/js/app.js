const form = document.getElementById("search-form");
const input = document.getElementById("query");
const button = document.getElementById("search-button");
const area = document.getElementById("result-area");
const count = document.getElementById("result-count");

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function showMessage(message, isError = false) {
  area.innerHTML = `<div class="status-message${isError ? " error" : ""}">${escapeHTML(message)}</div>`;
  count.textContent = "0";
}

function renderResults(payload) {
  count.textContent = payload.count;
  if (!payload.results.length) {
    showMessage(payload.message || "No matching documents found.");
    return;
  }
  area.innerHTML = payload.results.map((result) => `
    <article class="result-card">
      <div class="result-top">
        <span class="doc-name">${escapeHTML(result.document)}</span>
        <span class="score">RELEVANCE · ${result.score}</span>
      </div>
      <div class="matched">${result.matched_terms.map(term =>
        `<span class="term-tag">${escapeHTML(term)}</span>`).join("")}</div>
      <p class="preview">${escapeHTML(result.preview)}</p>
    </article>
  `).join("");
}

async function performSearch(query) {
  if (!query.trim()) {
    showMessage("Please enter a term or wildcard pattern.");
    input.focus();
    return;
  }
  button.disabled = true;
  button.querySelector("span").textContent = "Searching…";
  area.innerHTML = '<div class="status-message">Searching the inverted index…</div>';
  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query.trim())}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || payload.message || "Search failed.");
    renderResults(payload);
  } catch (error) {
    showMessage(error.message || "Unable to reach the search service.", true);
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Search";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  performSearch(input.value);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    input.value = chip.dataset.query;
    performSearch(input.value);
  });
});

async function loadStats() {
  try {
    const response = await fetch("/api/stats");
    const stats = await response.json();
    document.getElementById("doc-count").textContent = stats.document_count;
    document.getElementById("vocab-count").textContent = stats.vocabulary_size.toLocaleString();
    document.getElementById("occurrence-count").textContent = stats.indexed_terms.toLocaleString();
  } catch (_) {
    document.getElementById("doc-count").textContent = "—";
  }
}
loadStats();
