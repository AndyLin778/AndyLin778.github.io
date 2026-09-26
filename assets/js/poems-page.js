// 诗歌档案：日期节点、折线和原文展开。
(() => {
  const poems = Array.isArray(window.POEMS) ? window.POEMS : [];
  const list = document.getElementById("poemList");
  const yearsNav = document.getElementById("poemYears");
  const timeline = document.getElementById("poemTimeline");
  const line = document.getElementById("poemLine");
  if (!list || !yearsNav || !timeline || !line) return;

  const years = [...new Set(poems.map(poem => poem.date.slice(0, 4)))];
  document.getElementById("poemCount").textContent = String(poems.length).padStart(2, "0");
  document.getElementById("yearCount").textContent = String(years.length).padStart(2, "0");

  const excerptOf = (poem) => {
    const lines = poem.body.split("\n").map(line => line.trim())
      .filter(line => line && !line.startsWith("### ") && !line.startsWith("- Andy.Z"));
    const start = lines[0]?.includes(poem.title) || lines[0]?.startsWith("【") ? 1 : 0;
    return lines.slice(start, start + 2).join(" / ");
  };

  let index = 0;
  for (const year of years) {
    const link = document.createElement("a");
    link.href = `#year-${year}`;
    link.textContent = year;
    yearsNav.append(link);

    const group = document.createElement("section");
    group.className = "poem-year";
    group.id = `year-${year}`;

    const heading = document.createElement("h2");
    heading.className = "poem-year-label mono";
    heading.textContent = year;
    group.append(heading);

    for (const poem of poems.filter(item => item.date.startsWith(year))) {
      const side = index % 2 === 0 ? "left" : "right";
      const wrap = document.createElement("div");
      wrap.className = `poem-step poem-step--${side}`;

      const lineCount = poem.body.split("\n").filter(line => line.trim()).length;
      const shortPoem = lineCount <= 7 && poem.body.length <= 100;
      const details = document.createElement(shortPoem ? "article" : "details");
      details.className = shortPoem ? "poem-card poem-card--short" : "poem-card";
      const summary = document.createElement(shortPoem ? "div" : "summary");
      summary.className = "poem-summary";

      const pin = document.createElement("span");
      pin.className = "poem-pin";
      pin.setAttribute("aria-hidden", "true");
      summary.append(pin);

      const date = document.createElement("span");
      date.className = "poem-date mono";
      date.textContent = poem.date.replaceAll("-", ".") + (poem.time ? `  /  ${poem.time}` : "");
      summary.append(date);

      const title = document.createElement("strong");
      title.className = "poem-title";
      title.textContent = poem.title;
      summary.append(title);

      const excerpt = document.createElement("span");
      excerpt.className = shortPoem ? "poem-excerpt poem-excerpt--full" : "poem-excerpt";
      if (shortPoem) {
        excerpt.textContent = poem.body;
      } else {
        excerpt.textContent = excerptOf(poem);
      }
      summary.append(excerpt);

      const action = document.createElement("span");
      action.className = "poem-action mono";
      action.textContent = shortPoem ? `全文 / ${String(lineCount).padStart(2, "0")} 行` : "展开全文  ↗";
      summary.append(action);

      details.append(summary);
      if (!shortPoem) {
        const full = document.createElement("div");
        full.className = "poem-full";
        full.textContent = poem.body.replace(/^### /gm, "");
        details.append(full);
        details.addEventListener("toggle", () => {
          action.textContent = details.open ? "收起全文  ↖" : "展开全文  ↗";
          requestAnimationFrame(drawLine);
        });
      }
      wrap.append(details);
      group.append(wrap);
      index++;
    }
    list.append(group);
  }

  let pending = false;
  function drawLine() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => {
      pending = false;
      const bounds = timeline.getBoundingClientRect();
      const points = [...timeline.querySelectorAll(".poem-pin")].map(pin => {
        const box = pin.getBoundingClientRect();
        return [box.left + box.width / 2 - bounds.left, box.top + box.height / 2 - bounds.top];
      });
      line.setAttribute("viewBox", `0 0 ${bounds.width} ${bounds.height}`);
      line.setAttribute("width", bounds.width);
      line.setAttribute("height", bounds.height);
      const path = points.map(([x, y], i) => `${i ? "L" : "M"} ${x.toFixed(1)} ${y.toFixed(1)}`).join(" ");
      line.querySelector("path").setAttribute("d", path);
    });
  }
  window.addEventListener("resize", drawLine);
  window.addEventListener("load", drawLine);
  if ("ResizeObserver" in window) new ResizeObserver(drawLine).observe(list);
  drawLine();
})();
