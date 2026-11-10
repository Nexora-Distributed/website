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
document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const text = document.getElementById(button.dataset.copy).textContent;
    const status = button.closest('.command-block').querySelector('[role="status"]');
    try {
      await navigator.clipboard.writeText(text);
      status.textContent = 'Copied to clipboard';
    } catch {
      status.textContent = 'Select the command to copy it manually.';
    }
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
