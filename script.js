// ===== 导航栏滚动高亮 =====
const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll(".nav-link");

// 使用 IntersectionObserver 监听各区块进入视口，高亮对应导航项
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach((link) => {
          link.classList.toggle("active", link.getAttribute("href") === "#" + id);
        });
      }
    });
  },
  { rootMargin: "-40% 0px -55% 0px" }
);

sections.forEach((section) => observer.observe(section));

// ===== 移动端导航菜单切换 =====
const navToggle = document.getElementById("navToggle");
const navLinksList = document.getElementById("navLinks");

navToggle.addEventListener("click", () => {
  navToggle.classList.toggle("open");
  navLinksList.classList.toggle("open");
});

// 点击菜单项后自动收起移动端菜单
navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    navToggle.classList.remove("open");
    navLinksList.classList.remove("open");
  });
});

// ===== 欢迎弹窗（页面加载 5 秒后弹出） =====
const welcomeModal = document.getElementById("welcomeModal");
const modalClose = document.getElementById("modalClose");

setTimeout(() => {
  welcomeModal.classList.add("show");
}, 5000);

modalClose.addEventListener("click", () => {
  welcomeModal.classList.remove("show");
});

// 点击弹窗遮罩区域也可以关闭
welcomeModal.addEventListener("click", (event) => {
  if (event.target === welcomeModal) {
    welcomeModal.classList.remove("show");
  }
});

// ===== 底部版权年份自动更新 =====
document.getElementById("year").textContent = new Date().getFullYear();
