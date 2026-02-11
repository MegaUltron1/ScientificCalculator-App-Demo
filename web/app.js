const exprInput = document.getElementById("expr");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");

function setError(msg) {
  errorEl.textContent = msg || "";
}

function setResult(val) {
  resultEl.textContent = val === null || val === undefined ? "" : String(val);
}

async function evaluateExpression(expression) {
  const res = await fetch("/api/eval", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || "Evaluation failed");
  }
  return data.value;
}

function insertText(text) {
  const start = exprInput.selectionStart ?? exprInput.value.length;
  const end = exprInput.selectionEnd ?? exprInput.value.length;
  const before = exprInput.value.slice(0, start);
  const after = exprInput.value.slice(end);
  exprInput.value = before + text + after;
  const pos = start + text.length;
  exprInput.setSelectionRange(pos, pos);
  exprInput.focus();
}

function backspace() {
  const start = exprInput.selectionStart ?? exprInput.value.length;
  const end = exprInput.selectionEnd ?? exprInput.value.length;
  if (start !== end) {
    insertText("");
    return;
  }
  if (start <= 0) return;
  const before = exprInput.value.slice(0, start - 1);
  const after = exprInput.value.slice(end);
  exprInput.value = before + after;
  const pos = start - 1;
  exprInput.setSelectionRange(pos, pos);
  exprInput.focus();
}

async function doEquals() {
  setError("");
  const expression = exprInput.value.trim();
  if (!expression) return;
  try {
    const value = await evaluateExpression(expression);
    setResult(value);
  } catch (e) {
    setResult("");
    setError(e.message || String(e));
  }
}

document.querySelector(".keys").addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  const action = btn.dataset.action;
  const insert = btn.dataset.insert;
  if (action === "clear") {
    exprInput.value = "";
    setResult("");
    setError("");
    exprInput.focus();
    return;
  }
  if (action === "back") {
    backspace();
    return;
  }
  if (action === "equals") {
    await doEquals();
    return;
  }
  if (insert) {
    setError("");
    insertText(insert);
  }
});

exprInput.addEventListener("keydown", async (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    await doEquals();
  }
});

exprInput.focus();

