# -*- coding: utf-8 -*-
"""Generate a self-contained GenEd board exam website from questions.py."""
import json
import html
from questions import QUESTIONS

# Build JS array
data = []
for i, (subject, q, opts, answer, exp) in enumerate(QUESTIONS, 1):
    data.append({
        "id": i,
        "subject": subject,
        "q": q,
        "options": opts,
        "answer": answer,
        "exp": exp,
    })

QUESTIONS_JSON = json.dumps(data, ensure_ascii=False)

# Subject breakdown for the landing page
subjects = {}
for subject, *_ in QUESTIONS:
    subjects[subject] = subjects.get(subject, 0) + 1

def subject_chips():
    order = ["English", "Filipino", "Mathematics", "Science", "Social Science"]
    colors = {
        "English": ("#4f46e5", "#e0e7ff"),
        "Filipino": ("#b45309", "#fef3c7"),
        "Mathematics": ("#0f766e", "#ccfbf1"),
        "Science": ("#7c3aed", "#ede9fe"),
        "Social Science": ("#be123c", "#ffe4e6"),
    }
    chips = []
    for s in order:
        fg, bg = colors.get(s, ("#334155", "#e2e8f0"))
        chips.append(
            f'<div class="chip" style="color:{fg};background:{bg};border-color:{fg}">'
            f'<strong>{html.escape(s)}</strong> &middot; {subjects[s]} items</div>'
        )
    return "\n      ".join(chips)

CHIPS = subject_chips()
TOTAL = len(QUESTIONS)

# HTML with placeholders replaced
page = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>GenEd Board Exam Reviewer &middot; by Nendran Duke</title>
<meta name="description" content="150-item General Education board exam practice test for Education Generalists (LET GenEd), by Nendran Duke." />
<style>
  :root{
    --bg1:#eef2ff; --bg2:#fdf2f8; --ink:#0f172a; --muted:#64748b;
    --brand:#4f46e5; --brand2:#7c3aed; --good:#059669; --bad:#dc2626;
    --card:#ffffff; --line:#e2e8f0;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    background:linear-gradient(135deg,var(--bg1),var(--bg2));
    min-height:100vh; color:var(--ink); line-height:1.55;
  }
  .wrap{max-width:960px;margin:0 auto;padding:28px 18px 80px;}
  header.top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:18px;}
  .brand b{color:var(--brand);}
  .brand small{display:block;color:var(--muted);font-weight:600;letter-spacing:.4px;font-size:12px;text-transform:uppercase;}
  .badge-150{background:var(--brand);color:#fff;padding:8px 14px;border-radius:999px;font-weight:700;font-size:14px;box-shadow:0 6px 16px rgba(79,70,229,.28);}
  /* ---------- LANDING ---------- */
  .landing{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:30px 26px;box-shadow:0 20px 50px rgba(15,23,42,.08);}
  .landing h1{margin:0 0 6px;font-size:30px;line-height:1.2;}
  .landing h1 span{background:linear-gradient(90deg,var(--brand),var(--brand2));-webkit-background-clip:text;background-clip:text;color:transparent;}
  .authorline{color:var(--muted);margin:0 0 14px;font-size:15px;}
  .authorline b{color:var(--ink);}
  .chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;}
  .chip{font-size:13px;font-weight:600;padding:7px 12px;border-radius:999px;border:1px solid var(--line);}
  .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0;}
  .fact{background:#f8fafc;border:1px solid var(--line);border-radius:14px;padding:12px 14px;}
  .fact .num{font-size:22px;font-weight:800;color:var(--brand);}
  .fact .lbl{font-size:12px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.3px;}
  .instructions{background:#f8fafc;border:1px solid var(--line);border-radius:14px;padding:16px 18px;font-size:14px;color:#334155;}
  .instructions h3{margin:0 0 8px;font-size:15px;}
  .instructions ol{margin:0;padding-left:20px;}
  .instructions li{margin:4px 0;}
  .cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px;}
  .btn{border:none;cursor:pointer;font-weight:700;border-radius:12px;padding:13px 22px;font-size:15px;transition:transform .08s ease,box-shadow .12s ease;font-family:inherit;}
  .btn:active{transform:translateY(1px);}
  .btn-primary{background:linear-gradient(90deg,var(--brand),var(--brand2));color:#fff;box-shadow:0 10px 24px rgba(79,70,229,.32);}
  .btn-ghost{background:#fff;color:var(--ink);border:1px solid var(--line);}
  .btn-ghost:hover{background:#f8fafc;}
  .btn[disabled]{opacity:.5;cursor:not-allowed;}
  /* ---------- EXAM ---------- */
  .exam{display:none;}
  .toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px;}
  .progress-wrap{flex:1;min-width:200px;}
  .progress-info{display:flex;justify-content:space-between;font-size:13px;color:var(--muted);margin-bottom:6px;font-weight:600;}
  .bar{height:10px;background:#e2e8f0;border-radius:999px;overflow:hidden;}
  .bar>span{display:block;height:100%;background:linear-gradient(90deg,var(--brand),var(--brand2));width:0%;transition:width .25s ease;}
  .timer{font-variant-numeric:tabular-nums;font-weight:700;color:var(--brand);font-size:15px;background:#eef2ff;padding:8px 14px;border-radius:12px;}
  .card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:0 14px 34px rgba(15,23,42,.06);}
  .qmeta{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:16px;}
  .qnum{font-weight:800;font-size:18px;color:var(--brand);}
  .qsubject{font-size:12px;font-weight:700;padding:6px 12px;border-radius:999px;background:#eef2ff;color:var(--brand);}
  .qtxt{font-size:19px;font-weight:600;margin:6px 0 20px;}
  .opts{display:flex;flex-direction:column;gap:12px;}
  .opt{display:flex;gap:12px;align-items:flex-start;border:2px solid var(--line);border-radius:14px;padding:14px 16px;cursor:pointer;background:#fff;transition:border-color .12s ease,background .12s ease;}
  .opt:hover{border-color:#c7d2fe;background:#fafaff;}
  .opt .key{width:28px;height:28px;flex:0 0 28px;border-radius:50%;background:#f1f5f9;color:#475569;font-weight:700;display:grid;place-items:center;font-size:13px;border:1px solid var(--line);}
  .opt .txt{flex:1;font-size:15px;}
  .opt.sel{border-color:var(--brand);background:#eef2ff;}
  .opt.sel .key{background:var(--brand);color:#fff;border-color:var(--brand);}
  .opt .check{margin-left:auto;color:var(--brand);font-weight:800;align-self:center;opacity:0;}
  .opt.sel .check{opacity:1;}
  .nav{display:flex;justify-content:space-between;gap:12px;margin-top:22px;}
  .palette{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 20px;margin-top:16px;box-shadow:0 14px 34px rgba(15,23,42,.06);}
  .palette h3{margin:0 0 12px;font-size:15px;color:var(--muted);}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(44px,1fr));gap:8px;max-height:260px;overflow:auto;padding:2px;}
  .cell{height:42px;border-radius:10px;font-weight:700;font-size:14px;cursor:pointer;border:1px solid var(--line);background:#fff;color:#475569;display:grid;place-items:center;transition:background .1s;}
  .cell.done{background:#d1fae5;color:var(--good);border-color:#6ee7b7;}
  .cell.cur{outline:3px solid var(--brand);outline-offset:1px;background:#eef2ff;color:var(--brand);}
  .legend{display:flex;gap:18px;flex-wrap:wrap;margin-top:12px;font-size:13px;color:var(--muted);}
  .legend i{display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:6px;vertical-align:middle;}
  .submitrow{text-align:center;margin-top:20px;}
  /* ---------- RESULT ---------- */
  .result{display:none;}
  .score-hero{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-radius:20px;padding:30px;text-align:center;box-shadow:0 20px 50px rgba(79,70,229,.32);}
  .score-hero .big{font-size:56px;font-weight:900;line-height:1;}
  .score-hero .pct{font-size:20px;font-weight:700;opacity:.92;}
  .score-hero .rate{font-size:15px;font-weight:600;background:rgba(255,255,255,.18);display:inline-block;padding:6px 16px;border-radius:999px;margin-top:12px;}
  .stat-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:18px 0;}
  .stat{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;text-align:center;}
  .stat .v{font-size:28px;font-weight:800;color:var(--ink);}
  .stat .v.g{color:var(--good);} .stat .v.r{color:var(--bad);}
  .stat .t{font-size:12px;color:var(--muted);font-weight:700;text-transform:uppercase;}
  .subject-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:18px 0;}
  .scard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;}
  .scard .name{font-weight:700;font-size:15px;}
  .scard .sub{font-size:13px;color:var(--muted);margin:2px 0 10px;}
  .mini{height:8px;background:#e2e8f0;border-radius:999px;overflow:hidden;}
  .mini>span{display:block;height:100%;background:var(--brand);border-radius:999px;}
  .note{font-size:13px;color:#475569;background:#f8fafc;border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:14px 0;text-align:left;}
  .actions{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:20px;}
  /* ---------- REVIEW ---------- */
  .review{display:none;}
  .filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px;}
  .fbtn{border:1px solid var(--line);background:#fff;padding:9px 16px;border-radius:999px;font-weight:700;font-size:14px;cursor:pointer;color:var(--muted);}
  .fbtn.act{background:var(--brand);color:#fff;border-color:var(--brand);}
  .rq{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;margin-bottom:14px;}
  .rq .rh{display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap;}
  .rq .tag{font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;}
  .tag.right{background:#d1fae5;color:var(--good);}
  .tag.wrong{background:#fee2e2;color:var(--bad);}
  .tag.skip{background:#f1f5f9;color:var(--muted);}
  .rq .subject{font-size:12px;color:var(--muted);font-weight:600;}
  .rq .q{font-weight:600;font-size:16px;margin:6px 0 12px;}
  .rline{display:flex;gap:10px;align-items:flex-start;margin:6px 0;font-size:14px;}
  .rline .mark{font-weight:800;}
  .rline.correct .mark{color:var(--good);}
  .rline.wrong .mark{color:var(--bad);}
  .rline.sel{background:#eef2ff;padding:6px 10px;border-radius:8px;}
  .exp{background:#f8fafc;border-left:4px solid var(--brand);padding:10px 14px;border-radius:0 10px 10px 0;font-size:13.5px;color:#334155;margin-top:10px;}
  .exp b{color:var(--brand);}
  @media(max-width:560px){
    .landing h1{font-size:24px;}
    .qtxt{font-size:17px;}
    .card,.landing{padding:18px;}
    .nav{flex-direction:column-reverse;}
    .nav .btn{width:100%;}
  }
  .hidden{display:none!important;}
  .center{text-align:center;}
  footer{text-align:center;color:var(--muted);font-size:13px;margin-top:40px;}
  /* ---------- MODAL ---------- */
  .modal-overlay{position:fixed;inset:0;background:rgba(15,23,42,.55);display:flex;align-items:center;justify-content:center;z-index:100;padding:20px;}
  .modal{background:#fff;border-radius:18px;max-width:420px;width:100%;padding:24px;box-shadow:0 30px 70px rgba(15,23,42,.35);animation:pop .18s ease;}
  @keyframes pop{from{transform:scale(.94);opacity:0;}to{transform:scale(1);opacity:1;}}
  .modal h3{margin:0 0 10px;font-size:19px;}
  .modal p{margin:0 0 20px;color:#475569;font-size:15px;}
  .modal .mrow{display:flex;gap:10px;justify-content:flex-end;}
  .modal .btn{padding:11px 18px;}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand">
      <b>NENDRAN DUKE</b>
      <small>GenEd Reviewer Studio</small>
    </div>
    <div class="badge-150">150-Item Board Exam</div>
  </header>

  <!-- ============ LANDING ============ -->
  <section class="landing" id="landing">
    <h1>General Education <span>Board Exam</span> Reviewer</h1>
    <p class="authorline">Practice test for <b>Education Generalists</b> &middot; by <b>Nendran Duke</b></p>
    <div class="chips">
      __CHIPS__
    </div>
    <div class="facts">
      <div class="fact"><div class="num">__TOTAL__</div><div class="lbl">Total Items</div></div>
      <div class="fact"><div class="num">4</div><div class="lbl">Choices / Item</div></div>
      <div class="fact"><div class="num">5</div><div class="lbl">Subject Areas</div></div>
      <div class="fact"><div class="num">0</div><div class="lbl">Time Limit</div></div>
    </div>
    <div class="instructions">
      <h3>How to take this exam</h3>
      <ol>
        <li>Read each question and choose <b>one</b> best answer.</li>
        <li>Use <b>Next / Previous</b> or click a number in the palette to move around.</li>
        <li>You may skip items and return to them at any time.</li>
        <li>When you have answered every item, press <b>Submit</b> to see your score.</li>
      </ol>
    </div>
    <div class="cta">
      <button class="btn btn-primary" onclick="startExam()">Start Exam &#10132;</button>
      <button class="btn btn-ghost" onclick="window.print()">Print / Save PDF</button>
    </div>
  </section>

  <!-- ============ EXAM ============ -->
  <section class="exam" id="exam">
    <div class="toolbar">
      <div class="progress-wrap">
        <div class="progress-info"><span id="progText">0 of __TOTAL__ answered</span><span id="progPct">0%</span></div>
        <div class="bar"><span id="progBar"></span></div>
      </div>
      <div class="timer" id="timer">00:00</div>
    </div>

    <div class="card">
      <div class="qmeta">
        <div class="qnum">Question <span id="qnum">1</span> / __TOTAL__</div>
        <div class="qsubject" id="qsubject">English</div>
      </div>
      <div class="qtxt" id="qtxt"></div>
      <div class="opts" id="opts"></div>
      <div class="nav">
        <button class="btn btn-ghost" id="btnPrev" onclick="prevQ()">&larr; Previous</button>
        <button class="btn btn-primary" id="btnNext" onclick="nextQ()">Next &rarr;</button>
      </div>
    </div>

    <div class="palette">
      <h3>Question Palette</h3>
      <div class="grid" id="palette"></div>
      <div class="legend">
        <span><i style="background:#fff;border:1px solid var(--line)"></i> Unanswered</span>
        <span><i style="background:#d1fae5"></i> Answered</span>
        <span><i style="background:#eef2ff;border:3px solid var(--brand);outline:1px solid var(--brand)"></i> Current</span>
      </div>
    </div>

    <div class="submitrow">
      <button class="btn btn-primary" style="padding:14px 34px;font-size:17px;" onclick="confirmSubmit()">Submit Exam</button>
    </div>
  </section>

  <!-- ============ RESULT ============ -->
  <section class="result" id="result">
    <div class="score-hero">
      <div style="font-size:14px;font-weight:700;letter-spacing:1px;text-transform:uppercase;opacity:.9;">Your Score</div>
      <div class="big" id="scoreBig">0</div>
      <div class="pct" id="scorePct">0%</div>
      <div class="rate" id="rate">—</div>
    </div>
    <div class="stat-cards">
      <div class="stat"><div class="v g" id="stCorrect">0</div><div class="t">Correct</div></div>
      <div class="stat"><div class="v r" id="stWrong">0</div><div class="t">Wrong</div></div>
      <div class="stat"><div class="v" id="stSkip">0</div><div class="t">Unanswered</div></div>
      <div class="stat"><div class="v" id="stTime">0s</div><div class="t">Time</div></div>
    </div>
    <h3 style="font-size:17px;margin:6px 0;">Performance by Subject</h3>
    <div class="subject-cards" id="subjectCards"></div>
    <div class="note" id="passNote"></div>
    <div class="actions">
      <button class="btn btn-primary" onclick="showReview()">Review Answers</button>
      <button class="btn btn-ghost" onclick="retake()">Retake Exam</button>
    </div>
    <div style="text-align:center;margin-top:20px;color:var(--muted);font-size:13px;">Prepared by <b>Nendran Duke</b> &middot; GenEd Reviewer Studio</div>
  </section>

  <!-- ============ REVIEW ============ -->
  <section class="review" id="review">
    <h2 style="margin:0 0 16px;">Answer Review</h2>
    <div class="filters">
      <button class="fbtn act" data-f="all" onclick="setFilter('all')">All (__TOTAL__)</button>
      <button class="fbtn" data-f="wrong" onclick="setFilter('wrong')">Wrong</button>
      <button class="fbtn" data-f="right" onclick="setFilter('right')">Correct</button>
      <button class="fbtn" data-f="skip" onclick="setFilter('skip')">Unanswered</button>
      <button class="fbtn" data-f="all" onclick="showResult()">Back to Results</button>
    </div>
    <div id="reviewList"></div>
  </section>

  <footer>General Education Board Exam Reviewer &middot; Built for Education Generalists &middot; by Nendran Duke</footer>
</div>

<!-- ============ MODAL ============ -->
<div class="modal-overlay hidden" id="modal">
  <div class="modal">
    <h3 id="modalTitle">Are you sure?</h3>
    <p id="modalMsg"></p>
    <div class="mrow">
      <button class="btn btn-ghost" id="modalNo">Cancel</button>
      <button class="btn btn-primary" id="modalYes">Submit Exam</button>
    </div>
  </div>
</div>

<script>
const QUESTIONS = __QUESTIONS_JSON__;
const TOTAL = QUESTIONS.length;
const LETTERS = ["A","B","C","D"];
const SUBJCOL = {
  "English":"#4f46e5","Filipino":"#b45309","Mathematics":"#0f766e",
  "Science":"#7c3aed","Social Science":"#be123c"
};

let answers = new Array(TOTAL).fill(null);
let current = 0;
let timer = 0, timerId = null, started = false;
let filter = "all";

function startExam(){
  document.getElementById("landing").classList.add("hidden");
  document.getElementById("exam").classList.remove("hidden");
  buildPalette();
  render();
  if(!started){ started = true; timerId = setInterval(tick, 1000); }
}
function tick(){ timer++; const m=String(Math.floor(timer/60)).padStart(2,"0"), s=String(timer%60).padStart(2,"0"); document.getElementById("timer").textContent = m+":"+s; }

function buildPalette(){
  const g = document.getElementById("palette"); g.innerHTML="";
  QUESTIONS.forEach((q,i)=>{
    const c = document.createElement("button");
    c.className="cell"; c.textContent=i+1; c.dataset.i=i;
    c.onclick=()=>{ current=i; render(); };
    g.appendChild(c);
  });
}

function render(){
  const q = QUESTIONS[current];
  document.getElementById("qnum").textContent = current+1;
  document.getElementById("qsubject").textContent = q.subject;
  document.getElementById("qsubject").style.color = SUBJCOL[q.subject]||"var(--brand)";
  document.getElementById("qtxt").textContent = q.q;

  const box = document.getElementById("opts"); box.innerHTML="";
  q.options.forEach((op,i)=>{
    const o=document.createElement("div");
    o.className="opt"+(answers[current]===i?" sel":""); o.dataset.i=i;
    o.innerHTML = '<div class="key">'+LETTERS[i]+'</div><div class="txt"></div><div class="check">&#10003;</div>';
    o.querySelector(".txt").textContent = op;
    o.onclick = ()=>{ answers[current]=i; render(); };
    box.appendChild(o);
  });

  document.getElementById("btnPrev").disabled = current===0;
  document.getElementById("btnNext").textContent = current===TOTAL-1 ? "Finish" : "Next \u2192";

  paletteCells();
  updateProgress();
  window.scrollTo({top:0,behavior:"smooth"});
}
function paletteCells(){
  const cells=document.querySelectorAll("#palette .cell");
  cells.forEach((c,i)=>{
    c.classList.toggle("done", answers[i]!==null);
    c.classList.toggle("cur", i===current);
  });
}
function updateProgress(){
  const done = answers.filter(a=>a!==null).length;
  document.getElementById("progText").textContent = done+" of "+TOTAL+" answered";
  const pct = Math.round(done/TOTAL*100);
  document.getElementById("progPct").textContent = pct+"%";
  document.getElementById("progBar").style.width = pct+"%";
}

function nextQ(){ if(current<TOTAL-1){ current++; render(); } else { confirmSubmit(); } }
function prevQ(){ if(current>0){ current--; render(); } }

function confirmSubmit(){
  const done = answers.filter(a=>a!==null).length;
  const msg = done < TOTAL
    ? "You have answered "+done+" of "+TOTAL+" items. Unanswered items will be marked wrong. Submit anyway?"
    : "You have answered all "+TOTAL+" items. Submit your exam now?";
  showModal(msg, ()=>{ clearInterval(timerId); showResult(); });
}

function showModal(msg, onYes){
  const overlay = document.getElementById("modal");
  document.getElementById("modalMsg").textContent = msg;
  overlay.classList.remove("hidden");
  overlay.querySelector("#modalYes").onclick = ()=>{ overlay.classList.add("hidden"); onYes(); };
  overlay.querySelector("#modalNo").onclick = ()=>{ overlay.classList.add("hidden"); };
  overlay.addEventListener("click", function(ev){ if(ev.target===overlay){ overlay.classList.add("hidden"); } });
}

function compute(){
  let correct=0, wrong=0, skip=0;
  const bySub={};
  QUESTIONS.forEach((q,i)=>{
    const sub=q.subject;
    if(!bySub[sub]) bySub[sub]={total:0,correct:0,wrong:0,skip:0};
    bySub[sub].total++;
    const a=answers[i];
    if(a===null){ skip++; bySub[sub].skip++; }
    else if(a===q.answer){ correct++; bySub[sub].correct++; }
    else { wrong++; bySub[sub].wrong++; }
  });
  return {correct,wrong,skip,bySub};
}

function rating(pct){
  if(pct>=90) return "Outstanding \u2014 LET-ready";
  if(pct>=75) return "Very Good";
  if(pct>=60) return "Good \u2014 Keep reviewing";
  if(pct>=50) return "Fair \u2014 Needs more study";
  return "Needs substantial review";
}

function showResult(){
  document.getElementById("exam").classList.add("hidden");
  document.getElementById("review").classList.add("hidden");
  document.getElementById("result").classList.remove("hidden");

  const {correct,wrong,skip,bySub} = compute();
  const pct = Math.round(correct/TOTAL*100);
  document.getElementById("scoreBig").textContent = correct;
  document.getElementById("scorePct").textContent = pct+"%";
  document.getElementById("rate").textContent = rating(pct);
  document.getElementById("stCorrect").textContent = correct;
  document.getElementById("stWrong").textContent = wrong;
  document.getElementById("stSkip").textContent = skip;
  document.getElementById("stTime").textContent = fmtTime(timer);

  const sc = document.getElementById("subjectCards"); sc.innerHTML="";
  Object.keys(bySub).forEach(sub=>{
    const d=bySub[sub], p=Math.round(d.correct/d.total*100);
    const el=document.createElement("div");
    el.className="scard";
    el.innerHTML = '<div class="name" style="color:'+(SUBJCOL[sub]||"#334155")+'">'+sub+'</div>'+
      '<div class="sub">'+d.correct+'/'+d.total+' correct ('+p+'%)</div>'+
      '<div class="mini"><span style="width:'+p+'%;background:'+(SUBJCOL[sub]||"var(--brand)")+'"></span></div>';
    sc.appendChild(el);
  });

  document.getElementById("passNote").innerHTML = pct>=75
    ? "\u2705 <b>Great job!</b> At or above 75%, you are in strong shape for the GenEd portion of the LET. Review your mistakes below."
    : "\u26a0\ufe0f <b>Heads up:</b> A score below 75% hints you should revisit the subtopics you missed. Use the Review button to study the explanations.";
  window.scrollTo({top:0,behavior:"smooth"});
}

function fmtTime(s){ const m=Math.floor(s/60), sec=s%60; return m+":"+String(sec).padStart(2,"0"); }

function showReview(){
  document.getElementById("result").classList.add("hidden");
  document.getElementById("review").classList.remove("hidden");
  setFilter("all");
}
function setFilter(f){
  filter=f;
  document.querySelectorAll(".fbtn").forEach(b=>{
    if(b.textContent.trim()==="Back to Results") return;
    b.classList.toggle("act", b.dataset.f===f);
  });
  const list=document.getElementById("reviewList"); list.innerHTML="";
  QUESTIONS.forEach((q,i)=>{
    const a=answers[i];
    let cls="skip", label="Unanswered";
    if(a!==null){ cls=(a===q.answer)?"right":"wrong"; label=cls==="right"?"Correct":"Wrong"; }
    if(filter==="right"&&cls!=="right") return;
    if(filter==="wrong"&&cls!=="wrong") return;
    if(filter==="skip"&&cls!=="skip") return;
    const el=document.createElement("div"); el.className="rq";
    let optsHtml="";
    q.options.forEach((op,k)=>{
      const cc=(k===q.answer)?"correct":"";
      const ww=(a!==null&&k===a&&a!==q.answer)?"wrong":"";
      const sel=(a===k)?"sel":"";
      const mark=(k===q.answer)?"&#10003;":(a===k?"\u2715":"");
      optsHtml+='<div class="rline '+cc+' '+ww+' '+sel+'"><div class="mark">'+LETTERS[k]+'.</div><div>'+op+'</div>'+mark+'</div>';
    });
    el.innerHTML =
      '<div class="rh"><span class="tag '+cls+'">'+label+'</span>'+
      '<span class="subject">'+q.subject+'</span></div>'+
      '<div class="q">'+i+'. '+q.q+'</div>'+optsHtml+
      '<div class="exp"><b>Explanation:</b> '+q.exp+'</div>';
    list.appendChild(el);
  });
  if(!list.childElementCount){ list.innerHTML='<p style="color:var(--muted)">No questions match this filter.</p>'; }
  window.scrollTo({top:0,behavior:"smooth"});
}

function retake(){
  answers = new Array(TOTAL).fill(null);
  current=0; timer=0; filter="all";
  clearInterval(timerId);
  document.getElementById("review").classList.add("hidden");
  document.getElementById("result").classList.add("hidden");
  document.getElementById("landing").classList.remove("hidden");
  document.getElementById("exam").classList.add("hidden");
  started=false; timerId=null;
  document.getElementById("timer").textContent="00:00";
}
</script>
</body>
</html>
"""

page = page.replace("__CHIPS__", CHIPS)
page = page.replace("__TOTAL__", str(TOTAL))
page = page.replace("__QUESTIONS_JSON__", QUESTIONS_JSON)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)

print("Wrote index.html with", TOTAL, "questions.")
