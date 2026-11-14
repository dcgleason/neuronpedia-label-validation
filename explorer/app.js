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

function animateWidths(scope) {
  const els = scope.querySelectorAll("[data-w]");
  requestAnimationFrame(() => requestAnimationFrame(() => {
    for (const el of els) el.style.width = el.dataset.w + "%";
  }));
}

function countUp(el) {
  const target = Number(el.dataset.n);
  const start = performance.now();
  const dur = 900;
  const step = (now) => {
    const t = Math.min(1, (now - start) / dur);
    el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3))).toString();
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function barRow(label, passed, total, cls) {
  const p = total ? (passed / total) * 100 : 0;
  return `<div class="bar-row"><div class="bar-head"><span>${label}</span><span><strong>${passed} of ${total}</strong> passed (${pct(passed, total)}%)</span></div>` +
    `<div class="bar-track"><div class="bar-fill ${cls || ""}" data-w="${p}" style="width:0%"></div></div></div>`;
}

function classRow(label, g) {
  const fails = g.n - g.pass;
  if (!fails) return "";
  const w = (x) => (x / g.n) * 100;
  return `<div class="bar-row"><div class="bar-head"><span>${label}</span><span>${fails} failed of ${g.n}</span></div>` +
    `<div class="bar-track">` +
    `<div class="seg silent" data-w="${w(g.silent)}" style="width:0%"></div>` +
    `<div class="seg partial" data-w="${w(g.partial)}" style="width:0%"></div>` +
    `<div class="seg nmb" data-w="${w(g.nmb)}" style="width:0%"></div></div></div>`;
}

function renderStats() {
  const gemma = RECORDS.filter((r) => r.model === "Gemma-2-2B");
  const llama = RECORDS.filter((r) => r.model === "Llama 3.1 8B");
  const gp = gemma.filter((r) => r.verdict === "PASS").length;
  const lp = llama.filter((r) => r.verdict === "PASS").length;
  const su = gemma.filter((r) => r.predicted);
  const suRight = su.filter((r) => (r.predicted === "PASS") === (r.verdict === "PASS")).length;
  const cards = [
    [`<span class="countup" data-n="${gp}">0</span> / ${gemma.length}`, `Gemma labels passed (${pct(gp, gemma.length)}%)`],
    [`<span class="countup" data-n="${lp}">0</span> / ${llama.length}`, `Llama labels passed (${pct(lp, llama.length)}%)`],
    [`<span class="countup" data-n="${suRight}">0</span> / ${su.length}`, `pre-registered predictions right, scale-up`],
    [`<span class="countup" data-n="15">0</span> / 21`, `corrected labels that passed on retest`],
  ];
  const sc = document.getElementById("statCards");
  sc.innerHTML =
    cards.map(([big, lbl]) => `<div class="stat"><span class="big">${big}</span><span class="lbl">${lbl}</span></div>`).join("");
  for (const el of sc.querySelectorAll(".countup")) countUp(el);

  const byLayer = groupStats(gemma, (r) => `Gemma layer ${r.layer}`);
  const llamaByLayer = groupStats(llama, (r) => `Llama layer ${r.layer}`);
  let bars = "";
  for (const layer of [6, 12, 18]) {
    const g = byLayer.get(`Gemma layer ${layer}`);
    if (g) bars += barRow(`Gemma-2-2B, layer ${layer}`, g.pass, g.n, "");
  }
  for (const layer of [8, 16, 24]) {
    const g = llamaByLayer.get(`Llama layer ${layer}`);
    if (g) bars += barRow(`Llama 3.1 8B, layer ${layer}`, g.pass, g.n, "llama");
  }
  const pb = document.getElementById("passBars");
  pb.innerHTML = bars;
  animateWidths(pb);

  const gAll = groupStats(gemma, () => "Gemma").get("Gemma");
  const lAll = groupStats(llama, () => "Llama").get("Llama");
  const cb = document.getElementById("classBars");
  cb.innerHTML =
    classRow("Gemma-2-2B (all layers)", gAll) + classRow("Llama 3.1 8B", lAll) +
    `<div class="legend"><span><span class="dot" style="background:var(--silent)"></span>Silent</span>` +
    `<span><span class="dot" style="background:var(--partial)"></span>Partial</span>` +
    `<span><span class="dot" style="background:var(--nmb)"></span>Near-miss beat</span></div>`;
  animateWidths(cb);
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
  document.getElementById("rows").innerHTML = rows.map((r) => {
    const cls = r.verdict === "PASS" ? "—" : r.failure_class;
    const pred = r.predicted || "—";
    return `<tr data-i="${RECORDS.indexOf(r)}"><td>${r.model}</td><td>${r.layer}</td><td>${r.index}</td>` +
      `<td>${r.label}</td><td>${pred}</td>` +
      `<td><span class="pill ${r.verdict === "PASS" ? "pass" : "fail"}">${r.verdict}</span></td>` +
      `<td>${cls}</td><td>${fmt(margin(r))}</td></tr>`;
  }).join("");
  for (const tr of document.querySelectorAll("#rows tr")) {
    tr.addEventListener("click", () => showDetail(RECORDS[Number(tr.dataset.i)], true));
  }
}

function promptBlock(tag, text, value, max, cls) {
  const w = max > 0 ? Math.max(2, (value / max) * 100) : 0;
  return `<div class="prompt"><span class="tag">${tag}</span> <span style="float:right"><strong>${fmt(value)}</strong></span>` +
    `<div class="ptext">${text}</div><div class="scorebar"><div class="${cls}" data-w="${w}" style="width:0%"></div></div></div>`;
}

function hashFor(r) {
  return `#f-${r.model === "Gemma-2-2B" ? "gemma" : "llama"}-${r.layer}-${r.index}`;
}

function showDetail(r, scroll) {
  const max = Math.max(...r.sf, ...r.nm);
  const verdictText = r.verdict === "PASS"
    ? `<span class="pill pass">PASSED</span>`
    : `<span class="pill fail">FAILED</span> (${r.failure_class})`;
  const pred = r.predicted ? `<p class="note">Pre-registered prediction: <strong>${r.predicted}</strong> &mdash; prediction was ${((r.predicted === "PASS") === (r.verdict === "PASS")) ? "right" : "wrong"}.</p>` : "";
  const d = document.getElementById("detail");
  d.innerHTML =
    `<h3>${r.model}, layer ${r.layer}, feature ${r.index}</h3>` +
    `<p><strong>Label:</strong> &ldquo;${r.label}&rdquo;</p>` +
    `<p>Verdict: ${verdictText}. Margin (weakest should-fire minus strongest near-miss): <strong>${fmt(margin(r))}</strong>.</p>` +
    pred +
    promptBlock("Should fire 1", r.sf_prompts[0], r.sf[0], max, "sf-color") +
    promptBlock("Should fire 2", r.sf_prompts[1], r.sf[1], max, "sf-color") +
    promptBlock("Near miss 1", r.nm_prompts[0], r.nm[0], max, "nm-color") +
    promptBlock("Near miss 2", r.nm_prompts[1], r.nm[1], max, "nm-color");
  d.hidden = false;
  history.replaceState(null, "", hashFor(r));
  animateWidths(d);
  if (scroll) d.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function openFromHash() {
  const withLayer = location.hash.match(/^#f-(gemma|llama)-(\d+)-(\d+)$/);
  if (withLayer) {
    const model = withLayer[1] === "gemma" ? "Gemma-2-2B" : "Llama 3.1 8B";
    const rec = RECORDS.find((r) => r.model === model && r.layer === Number(withLayer[2]) && r.index === Number(withLayer[3]));
    if (rec) { showDetail(rec, true); return; }
  }
  const m = location.hash.match(/^#f-(gemma|llama)-(\d+)$/);
  if (!m) return;
  const model = m[1] === "gemma" ? "Gemma-2-2B" : "Llama 3.1 8B";
  const rec = RECORDS.find((r) => r.model === model && r.index === Number(m[2]));
  if (rec) showDetail(rec, true);
}

function wireStoryButtons() {
  const ex = document.getElementById("btnExample");
  if (ex) ex.addEventListener("click", () => {
    const rec = RECORDS.find((r) => r.model === "Gemma-2-2B" && r.index === 5158);
    if (rec) showDetail(rec, true);
  });
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
    wireStoryButtons();
    openFromHash();
  })
  .catch((err) => {
    document.getElementById("countLine").textContent = "Could not load the results data (" + err.message + ").";
  });
