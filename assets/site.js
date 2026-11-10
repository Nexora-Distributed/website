document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    document.querySelectorAll('details[open]').forEach((item) => item.removeAttribute('open'));
    if (menuButton?.getAttribute('aria-expanded') === 'true') {
      menuButton.click();
      menuButton.focus();
    }
  }
});
document.addEventListener('click', (event) => {
  document.querySelectorAll('.nav-product[open]').forEach((item) => {
    if (!item.contains(event.target)) item.removeAttribute('open');
  });
});
document.querySelectorAll('[role="tablist"]').forEach((list) => {
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  const activate = (tab) => {
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', (event) => {
      const offsets = { ArrowRight: 1, ArrowLeft: -1 };
      let next;
      if (event.key in offsets) next = tabs[(index + offsets[event.key] + tabs.length) % tabs.length];
      if (event.key === 'Home') next = tabs[0];
      if (event.key === 'End') next = tabs[tabs.length - 1];
      if (next) {
        event.preventDefault();
        activate(next);
        next.focus();
      }
    });
  });
});
const search = document.querySelector('#capability-search');
search?.addEventListener('input', () => {
  let count = 0;
  const query = search.value.trim().toLowerCase();
  document.querySelectorAll('[data-capability]').forEach((item) => {
    const match = item.textContent.toLowerCase().includes(query);
    item.hidden = !match;
    if (match) count += 1;
  });
  document.querySelector('#search-status').textContent = `${count} capabilities shown`;
});

const motionButton = document.querySelector('.motion-toggle');
motionButton?.addEventListener('click', () => {
  const paused = motionButton.getAttribute('aria-pressed') !== 'true';
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.setAttribute('aria-label', paused ? 'Resume illustration animations' : 'Pause illustration animations');
  motionButton.querySelector('span').textContent = paused ? 'Resume motion' : 'Pause motion';
  document.documentElement.classList.toggle('motion-paused', paused);
  document.querySelectorAll('img[src*=".svg"]').forEach((image) => {
    const url = new URL(image.src);
    url.hash = paused ? 'still' : '';
    image.src = url.href;
  });
});
