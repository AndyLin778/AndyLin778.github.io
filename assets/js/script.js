// ============================================================
// 个人网站交互脚本（纯原生 JS，无依赖）
//   1. 首屏大字：逐字打出 → 停留 → 退格 → 换下一个词
//   2. 副标题打字机
//   3. 本地时间（导航 / 首屏 / 页脚）
//   4. 导航滚动高亮 + 移动端菜单
//   5. 滚动揭示、欢迎弹窗、页脚年份
// ============================================================

// ===== 想改内容，改这里就够了 =====
const HERO_WORDS = ["MY PAGE", "HELLO", "2026", "WEB DEV"]; // 首屏依次打出的大字
const TYPED_LINES = [                                        // 副标题循环播放的句子
  "把想法变成看得见的东西。",
  "持续学习，保持好奇。",
  "这里记录我的实验与作品。"
];

const reduceMotion = document.documentElement.hasAttribute("data-reduced");

// ------------------------------------------------------------
// 通用打字机：逐字打出 → 停留 → 逐字退回 → 下一句
//   timing：{ type 打字 / hold 整句停留 / del 退格 / pause 换句 }（毫秒）
//   cycles：播完几轮后停住（停住时稳稳留下第一句，并把光标淡出）
// ------------------------------------------------------------
function makeTyper(element, lines, timing, cycles) {
  if (!element) return;

  const finish = () => {
    element.classList.add("is-done");
    if (element.parentElement) element.parentElement.classList.add("is-done");
  };

  // 系统开了“减少动效”就直接显示第一句，不动
  if (reduceMotion) {
    element.textContent = lines[0];
    finish();
    return;
  }

  let index = 0;        // 当前第几句
  let count = 0;        // 当前句子已打出几个字
  let deleting = false; // 当前是不是在退格
  let seen = 0;         // 已经完整播完的句子数
  let finalTyping = false; // 收尾：最后再稳稳打出第一句
  element.textContent = "";

  function step() {
    const line = lines[index];

    if (!deleting) {
      count += 1;
      element.textContent = line.slice(0, count);
      if (count < line.length) {
        setTimeout(step, timing.type);
        return;
      }
      if (finalTyping) {
        finish();
        return;
      }
      deleting = true;
      setTimeout(step, timing.hold);
      return;
    }

    count -= 1;
    element.textContent = line.slice(0, count);
    if (count > 0) {
      setTimeout(step, timing.del);
      return;
    }

    deleting = false;
    seen += 1;
    if (seen >= lines.length * cycles) {
      // 播够了，收尾停在第一句
      index = 0;
      count = 0;
      finalTyping = true;
    } else {
      index = (index + 1) % lines.length;
    }
    setTimeout(step, timing.pause);
  }

  step();
}


// 首屏大字 + 副标题（各播 1 轮后停住，不再无限循环）
makeTyper(document.getElementById("heroWord"), HERO_WORDS,
  { type: 90, hold: 1600, del: 45, pause: 350 }, 1);
makeTyper(document.getElementById("typedText"), TYPED_LINES,
  { type: 110, hold: 1800, del: 40, pause: 420 }, 1);

// ------------------------------------------------------------
// 本地时间：导航栏、首屏、页脚三处一起走
// ------------------------------------------------------------
const navClock = document.getElementById("navClock");
const heroClock = document.getElementById("heroClock");
const footerClock = document.getElementById("footerClock");
const zoneText = document.querySelector(".hero-meta-left");

function pad(value) {
  return value < 10 ? "0" + value : String(value);
}

function updateClocks() {
  const now = new Date();
  const time = pad(now.getHours()) + ":" + pad(now.getMinutes()) + ":" + pad(now.getSeconds());
  const short = pad(now.getHours()) + ":" + pad(now.getMinutes());

  if (navClock) navClock.textContent = "LOCAL " + short;
  if (heroClock) heroClock.textContent = "LOCAL " + time;
  if (footerClock) footerClock.textContent = "LOCAL " + time;

  // 按本机时区算出 UTC 偏移，例如 UTC+08:00
  const offset = -now.getTimezoneOffset();
  const abs = Math.abs(offset);
  const zone = "UTC" + (offset < 0 ? "-" : "+") + pad(Math.floor(abs / 60)) + ":" + pad(abs % 60);
  if (zoneText) {
    zoneText.textContent = (offset === 480 ? "北京时间" : "本地时间") + " · " + zone;
  }
}

updateClocks();
setInterval(updateClocks, 1000);

// ------------------------------------------------------------
// 导航高亮：滚动时高亮当前所在区块
// ------------------------------------------------------------
const navLinksEl = document.getElementById("navLinks");
const navToggle = document.getElementById("navToggle");
const navLinkItems = document.querySelectorAll(".nav-link");
const sections = document.querySelectorAll("section[id]");

function highlightNav() {
  // 以视口 35% 高度处为基准线，落在哪一段就高亮哪一项
  const line = window.scrollY + window.innerHeight * 0.35;
  let current = sections[0] ? sections[0].id : "";
  sections.forEach((section) => {
    if (section.offsetTop <= line) current = section.id;
  });
  navLinkItems.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === "#" + current);
  });
}

if (navToggle && navLinksEl) {
  const closeMenu = () => {
    navLinksEl.classList.remove("open");
    navToggle.classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
  };

  navToggle.addEventListener("click", () => {
    const open = navLinksEl.classList.toggle("open");
    navToggle.classList.toggle("open", open);
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // 点了菜单项就自动收起
  navLinkItems.forEach((link) => link.addEventListener("click", closeMenu));
}

// 滚动时更新高亮
window.addEventListener("scroll", highlightNav, { passive: true });
highlightNav();

// ------------------------------------------------------------
// 滚动揭示：内容进入视口时横向展开（对应 ansyn 的 strip-in）
//   这里用「滚动事件 + 元素位置」判断，不用 IntersectionObserver：
//   被 clip-path 裁切过的元素可见面积为零，IO 会认为它一直“没进入视口”，
//   内容就永远不显示（这正是之前下方一片空白的元凶）。
// ------------------------------------------------------------
const revealItems = document.querySelectorAll(".reveal");

function revealVisible() {
  const limit = window.innerHeight * 0.88;
  revealItems.forEach((item) => {
    if (item.classList.contains("is-in")) return;
    if (item.getBoundingClientRect().top < limit) item.classList.add("is-in");
  });
}

if (revealItems.length) {
  window.addEventListener("scroll", revealVisible, { passive: true });
  window.addEventListener("resize", revealVisible);
  revealVisible(); // 首屏里已经在视口内的，进来就展开
}

// ------------------------------------------------------------
// 欢迎弹窗 + 页脚年份
// ------------------------------------------------------------
const welcomeModal = document.getElementById("welcomeModal");
const modalClose = document.getElementById("modalClose");

if (welcomeModal && modalClose) {
  setTimeout(() => welcomeModal.classList.add("show"), 5000);

  modalClose.addEventListener("click", () => welcomeModal.classList.remove("show"));

  // 点遮罩区域也可以关闭
  welcomeModal.addEventListener("click", (event) => {
    if (event.target === welcomeModal) welcomeModal.classList.remove("show");
  });
}

const yearEl = document.getElementById("year");
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

// 告诉 CSS：脚本已经正常接管所有交互（据此关掉“自动展开”的兜底动画）
document.documentElement.classList.add("ready");

