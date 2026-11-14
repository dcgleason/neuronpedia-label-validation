"use strict";

const fmt = (v) => (Math.round(v * 100) / 100).toString();
const pct = (a, b) => Math.round((a / b) * 1000) / 10;

let RECORDS = [];

function groupStats(records, keyFn) {
  const groups = new Map();
  for (const r of records) {
    const k = keyFn(r);
    if (!groups.has(k)) groups.set(k, { n: 0, pass: 0, silent: 0, partial: 0, nmb: 0 });
    const g = groups.get(k);
    g.n += 1;
    if (r.verdict === "PASS") g.pass += 1;
    else if (r.failure_class === "silent") g.silent += 1;
    else if (r.failure_class === "partial") g.partial += 1;
    else if (r.failure_class === "near-miss-beat") g.nmb += 1;
  }
  return groups;
}

function barRow(label, passed, total, cls) {
  const p = total ? (passed / total) * 100 : 0;
  return `<div class="bar-row"><div class="bar-head"><span>${label}</span><span><strong>${passed} of ${total}</strong> passed (${pct(passed, total)}%)</span></div>` +
    `<div class="bar-track"><div class="bar-fill ${cls || ""}" style="width:${p}%"></div></div></div>`;
}

function classRow(label, g) {
  const fails = g.n - g.pass;
  if (!fails) return "";
  const w = (x) => (x / g.n) * 100;
  return `<div class="bar-row"><div class="bar-head"><span>${label}</span><span>${fails} failed of ${g.n}</span></div>` +
    `<div class="bar-track">` +
    `<div class="seg silent" style="width:${w(g.silent)}%"></div>` +
    `<div class="seg partial" style="width:${w(g.partial)}%"></div>` +
    `<div class="seg nmb" style="width:${w(g.nmb)}%"></div></div></div>`;
}

function renderStats() {
  const gemma = RECORDS.filter((r) => r.model === "Gemma-2-2B");
  const llama = RECORDS.filter((r) => r.model === "Llama 3.1 8B");
  const gp = gemma.filter((r) => r.verdict === "PASS").length;
  const lp = llama.filter((r) => r.verdict === "PASS").length;
  const su = gemma.filter((r) => r.predicted);
  const suRight = su.filter((r) => (r.predicted === "PASS") === (r.verdict === "PASS")).length;
  const cards = [
    [`${gp} / ${gemma.length}`, `Gemma labels passed (${pct(gp, gemma.length)}%)`],
    [`${lp} / ${llama.length}`, `Llama labels passed (${pct(lp, llama.length)}%)`],
    [`${suRight} / ${su.length}`, `pre-registered predictions right, scale-up`],
    [`15 / 21`, `corrected labels that passed on retest`],
  ];
  document.getElementById("statCards").innerHTML =
    cards.map(([big, lbl]) => `<div class="stat"><span class="big">${big}</span><span class="lbl">${lbl}</span></div>`).join("");

  const byLayer = groupStats(gemma, (r) => `Gemma layer ${r.layer}`);
  const llamaStats = groupStats(llama, () => "Llama layer 16");
  let bars = "";
  for (const layer of [6, 12, 18]) {
    const g = byLayer.get(`Gemma layer ${layer}`);
    if (g) bars += barRow(`Gemma-2-2B, layer ${layer}`, g.pass, g.n, "");
  }
  const lg = llamaStats.get("Llama layer 16");
  if (lg) bars += barRow("Llama 3.1 8B, layer 16", lg.pass, lg.n, "llama");
  document.getElementById("passBars").innerHTML = bars;

  const gAll = groupStats(gemma, () => "Gemma").get("Gemma");
  const lAll = groupStats(llama, () => "Llama").get("Llama");
  document.getElementById("classBars").innerHTML =
    classRow("Gemma-2-2B (all layers)", gAll) + classRow("Llama 3.1 8B", lAll) +
    `<div class="legend"><span><span class="dot" style="background:var(--silent)"></span>Silent</span>` +
    `<span><span class="dot" style="background:var(--partial)"></span>Partial</span>` +
    `<span><span class="dot" style="background:var(--nmb)"></span>Near-miss beat</span></div>`;
}

function currentFilters() {
  return {
    q: document.getElementById("q").value.trim().toLowerCase(),
    model: document.getElementById("fModel").value,
    layer: document.getElementById("fLayer").value,
    verdict: document.getElementById("fVerdict").value,
    fclass: document.getElementById("fClass").value,
  };
}

function applyFilters() {
  const f = currentFilters();
  return RECORDS.filter((r) => {
    if (f.model && r.model !== f.model) return false;
    if (f.layer && String(r.layer) !== f.layer) return false;
    if (f.verdict && r.verdict !== f.verdict) return false;
    if (f.fclass && r.failure_class !== f.fclass) return false;
    if (f.q && !(r.label.toLowerCase().includes(f.q) || String(r.index).includes(f.q))) return false;
    return true;
  });
}

function margin(r) {
  return Math.min(...r.sf) - Math.max(...r.nm);
}

function renderTable() {
  const rows = applyFilters();
  document.getElementById("countLine").textContent = `Showing ${rows.length} of ${RECORDS.length} labels.`;
  document.getElementById("rows").innerHTML = rows.map((r, i) => {
    const cls = r.verdict === "PASS" ? "—" : r.failure_class;
    const pred = r.predicted || "—";
    return `<tr data-i="${RECORDS.indexOf(r)}"><td>${r.model}</td><td>${r.layer}</td><td>${r.index}</td>` +
      `<td>${r.label}</td><td>${pred}</td>` +
      `<td><span class="pill ${r.verdict === "PASS" ? "pass" : "fail"}">${r.verdict}</span></td>` +
      `<td>${cls}</td><td>${fmt(margin(r))}</td></tr>`;
  }).join("");
  for (const tr of document.querySelectorAll("#rows tr")) {
    tr.addEventListener("click", () => showDetail(RECORDS[Number(tr.dataset.i)]));
  }
}

function promptBlock(tag, text, value, max, cls) {
  const w = max > 0 ? Math.max(2, (value / max) * 100) : 0;
  return `<div class="prompt"><span class="tag">${tag}</span> <span style="float:right"><strong>${fmt(value)}</strong></span>` +
    `<div class="ptext">${text}</div><div class="scorebar"><div class="${cls}" style="width:${w}%"></div></div></div>`;
}

function showDetail(r) {
  const max = Math.max(...r.sf, ...r.nm);
  const verdictText = r.verdict === "PASS"
    ? `<span class="pill pass">PASSED</span>`
    : `<span class="pill fail">FAILED</span> (${r.failure_class})`;
  const pred = r.predicted ? `<p class="note">Pre-registered prediction: <strong>${r.predicted}</strong> &mdash; prediction was ${((r.predicted === "PASS") === (r.verdict === "PASS")) ? "right" : "wrong"}.</p>` : "";
  document.getElementById("detail").innerHTML =
    `<h3>${r.model}, layer ${r.layer}, feature ${r.index}</h3>` +
    `<p><strong>Label:</strong> &ldquo;${r.label}&rdquo;</p>` +
    `<p>Verdict: ${verdictText}. Margin (weakest should-fire minus strongest near-miss): <strong>${fmt(margin(r))}</strong>.</p>` +
    pred +
    promptBlock("Should fire 1", r.sf_prompts[0], r.sf[0], max, "sf-color") +
    promptBlock("Should fire 2", r.sf_prompts[1], r.sf[1], max, "sf-color") +
    promptBlock("Near miss 1", r.nm_prompts[0], r.nm[0], max, "nm-color") +
    promptBlock("Near miss 2", r.nm_prompts[1], r.nm[1], max, "nm-color");
  const d = document.getElementById("detail");
  d.hidden = false;
  d.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function initFilters() {
  const models = [...new Set(RECORDS.map((r) => r.model))];
  const layers = [...new Set(RECORDS.map((r) => r.layer))].sort((a, b) => a - b);
  document.getElementById("fModel").innerHTML =
    `<option value="">All models</option>` + models.map((m) => `<option>${m}</option>`).join("");
  document.getElementById("fLayer").innerHTML =
    `<option value="">All layers</option>` + layers.map((l) => `<option>${l}</option>`).join("");
  for (const id of ["q", "fModel", "fLayer", "fVerdict", "fClass"]) {
    document.getElementById(id).addEventListener("input", renderTable);
    document.getElementById(id).addEventListener("change", renderTable);
  }
}

fetch("data.json")
  .then((res) => res.json())
  .then((data) => {
    RECORDS = data.records;
    renderStats();
    initFilters();
    renderTable();
  })
  .catch((err) => {
    document.getElementById("countLine").textContent = "Could not load the results data (" + err.message + ").";
  });
