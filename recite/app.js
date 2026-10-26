(() => {
  'use strict';
  const units = window.RECITE_UNITS;
  const modules = [{id:'exams',name:'真题积累'}, {id:'predictions',name:'预测卷'}, {id:'weekly',name:'周测卷'}];
  const $ = id => document.getElementById(id);
  function textElement(tag, text, className) {
    const element = document.createElement(tag);
    element.textContent = text;
    if (className) element.className = className;
    return element;
  }
  function paragraph(part, label, english) {
    const body = textElement('p', english ? part.en : part.zh, english ? 'english' : '');
    if (english) body.lang = 'en';
    if (english && !part.core) {
      const context = document.createElement('div');
      context.className = 'letter-context'; context.append(body); return context;
    }
    const details = document.createElement('details');
    details.className = english ? 'paragraph' : 'paragraph translation';
    details.open = english;
    const summary = textElement('summary', label + (english ? '' : ' · 译文'));
    summary.append(textElement('span', '', 'fold-label'));
    details.append(summary, body);
    if (english && part.prefix) {
      const wrapper = document.createElement('div');
      const prefix = textElement('p', part.prefix, 'english letter-prefix'); prefix.lang = 'en';
      wrapper.append(prefix, details); return wrapper;
    }
    return details;
  }
  function catalog(moduleId, unit) {
    const members = units.filter(item => item.module === moduleId);
    $('catalog').replaceChildren(); $('unit-select').replaceChildren();
    $('count').textContent = members.length;
    $('module-heading').textContent = modules.find(item => item.id === moduleId).name;
    $('unit-select').disabled = !members.length;
    members.forEach(item => {
      const link = textElement('a', '', 'catalog-link'); link.href = '#' + item.id;
      link.append(textElement('small', item.category), item.title);
      if (item.id === unit?.id) link.setAttribute('aria-current', 'page');
      $('catalog').append(link);
      const option = textElement('option', item.category + ' · ' + item.title.replace(/^\d{4} · /, ''));
      option.value = item.id; $('unit-select').append(option);
    });
    if (!members.length) $('unit-select').append(textElement('option', '待补充'));
    document.querySelectorAll('.module-link').forEach(link => {
      if (link.dataset.module === moduleId) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  }
  function render() {
    const hash = location.hash.slice(1);
    let unit = units.find(item => item.id === hash);
    const requestedModule = hash.startsWith('module/') ? hash.slice(7) : null;
    const moduleId = unit?.module || (modules.some(item => item.id === requestedModule) ? requestedModule : 'exams');
    unit ||= units.find(item => item.module === moduleId);
    catalog(moduleId, unit);
    $('reader').hidden = !unit; $('empty-module').hidden = !!unit;
    if (!unit) { document.title = '周测卷 · 作文背诵'; return; }
    document.title = unit.title + ' · 作文背诵';
    $('category').textContent = unit.category;
    $('essay-title').textContent = unit.title;
    $('source').textContent = unit.source;
    $('content-note').textContent = unit.note || '';
    $('prompt').textContent = unit.prompt;
    $('unit-select').value = unit.id;
    $('prompt-figure').hidden = !unit.image;
    if (unit.image) {
      $('prompt-image').src = unit.image; $('prompt-image').alt = unit.imageAlt;
      $('image-link').href = unit.image;
      $('image-caption').textContent = unit.imageCaption || '资料站重绘 / 转录配图 · 点击查看大图';
    } else {
      $('prompt-image').removeAttribute('src'); $('image-link').removeAttribute('href');
    }
    $('approach').open = false;
    $('approach-list').replaceChildren(...unit.approach.map(text => textElement('li', text)));
    const small = unit.part === 'A';
    $('paragraphs').classList.toggle('letter', small);
    $('expand-all').textContent = small ? '展开核心' : '全部展开';
    $('collapse-all').textContent = small ? '收起核心' : '全部收起';
    $('recall-note').textContent = small ? '只收起核心内容；称呼、客套与落款保留，沿着完整行文回忆。' : '';
    let coreIndex = 0;
    const labels = unit.paragraphs.map((part, i) => small ? (part.core ? `核心段落 ${++coreIndex}` : (i === 0 ? '开场 / 标题' : '收尾 / 落款')) : `第 ${i + 1} 段`);
    $('paragraphs').replaceChildren(...unit.paragraphs.map((part, i) => paragraph(part, labels[i], true)));
    $('translations').replaceChildren(...unit.paragraphs.map((part, i) => paragraph(part, labels[i], false)));
    $('materials-section').hidden = !unit.materials?.length;
    $('materials').replaceChildren(...(unit.materials || []).map(item => {
      const block = document.createElement('div'); block.className = 'material';
      const en = textElement('p', item.en, 'material-en'); en.lang = 'en';
      block.append(en, textElement('p', item.zh), textElement('p', item.use, 'source'));
      return block;
    }));
  }
  modules.forEach(module => {
    const link = textElement('a', module.name, 'module-link');
    link.href = '#module/' + module.id; link.dataset.module = module.id;
    $('modules').append(link);
  });
  $('unit-select').addEventListener('change', event => { location.hash = event.target.value; });
  $('expand-all').addEventListener('click', () => document.querySelectorAll('#paragraphs details').forEach(p => p.open = true));
  $('collapse-all').addEventListener('click', () => document.querySelectorAll('#paragraphs details').forEach(p => p.open = false));
  window.addEventListener('hashchange', render);
  render();
})();
