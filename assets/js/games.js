// ============================================================
// 游戏目录数据
//
// 加一个游戏：在下面数组里照抄一行，改掉内容即可。
//   title     中文名（或主标题）
//   subtitle  英文名 / 副标题，可以不写
//   tag       类型标签，可以不写
//   page      这个游戏详情页的文件名；还没写就留空 ""
//   cover     封面图路径，例如 "covers/dsp.jpg"；留空则显示首字占位
//
// 留空 page 的卡片会显示「待写」，不会变成可点击的链接。
// ============================================================

const GAMES = [
  // ---- 第一组（截图里的「11」分类）----
  { title: "戴森球计划",              subtitle: "Dyson Sphere Program",            tag: "模拟 / 建造",   page: "", cover: "" },
  { title: "饥荒联机版",              subtitle: "Don't Starve Together",           tag: "生存 / 联机",   page: "", cover: "" },
  { title: "缺氧",                    subtitle: "Oxygen Not Included",             tag: "模拟 / 经营",   page: "", cover: "" },
  { title: "深岩银河",                subtitle: "Deep Rock Galactic",              tag: "合作 / 射击",   page: "", cover: "" },
  { title: "英雄联盟",                subtitle: "League of Legends",               tag: "MOBA / 竞技",   page: "", cover: "" },
  { title: "Counter-Strike 2",        subtitle: "CS2",                             tag: "射击 / 竞技",   page: "", cover: "" },
  { title: "Grounded",                subtitle: "禁闭求生",                        tag: "生存 / 合作",   page: "", cover: "" },

  // ---- 未分类 ----
  { title: "逃离鸭科夫",              subtitle: "Escape From Duckov",              tag: "射击 / 撤离",   page: "", cover: "" },
  { title: "ASTRONEER",               subtitle: "异星探险家",                      tag: "探索 / 建造",   page: "", cover: "" },
  { title: "Project Zomboid",         subtitle: "僵尸毁灭工程",                    tag: "生存 / 沙盒",   page: "", cover: "" },
  { title: "Raft",                    subtitle: "木筏求生",                        tag: "生存 / 合作",   page: "", cover: "" },
  { title: "Sid Meier's Civilization VI", subtitle: "文明六",                       tag: "策略 / 回合制", page: "", cover: "" },
  { title: "Stardew Valley",          subtitle: "星露谷物语",                      tag: "模拟 / 经营",   page: "", cover: "" }
];

// ============================================================
// 下面是把数据渲染成卡片的代码，一般不用改
// ============================================================
(function renderGames() {
  const grid = document.getElementById("gameGrid");
  if (!grid) return;

  const escape = (text) =>
    String(text).replace(/[&<>"]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));

  grid.innerHTML = GAMES.map((game) => {
    const initial = escape((game.title || "?").trim().charAt(0).toUpperCase());
    const cover = game.cover
      ? '<img src="' + escape(game.cover) + '" alt="' + escape(game.title) + ' 封面">'
      : "<span>" + initial + "</span>";

    const inner =
      '<div class="game-cover">' + cover + "</div>" +
      '<div class="game-body">' +
        '<h3 class="game-title">' + escape(game.title) + "</h3>" +
        (game.subtitle ? '<p class="game-sub mono">' + escape(game.subtitle) + "</p>" : "") +
        (game.tag ? '<p class="game-tag mono">' + escape(game.tag) + "</p>" : "") +
      "</div>" +
      '<p class="game-state mono">' + (game.page ? "笔记 ↗" : "待写") + "</p>";

    return game.page
      ? '<a class="game-card is-ready" href="' + escape(game.page) + '">' + inner + "</a>"
      : '<article class="game-card">' + inner + "</article>";
  }).join("");

  // 首页 / 其它页面想显示数量时，放一个 id="gameCount" 的元素即可
  const counter = document.getElementById("gameCount");
  if (counter) counter.textContent = GAMES.length;
})();
