"""A consistent 24px outline SVG icon family."""

PATHS = {'arrow': 'M7 17 17 7M7 7h10v10', 'chevron': 'm6 9 6 6 6-6', 'check': 'm5 12 4 4L19 6', 'menu': 'M4 6h16M4 12h16M4 18h16', 'grid': 'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z', 'network': 'M4 4h6v6H4zM14 14h6v6h-6zM7 10v7h7M17 4v6M14 7h6', 'chart': 'M4 4v16h16M8 15v-4M12 15V7M16 15v-6', 'shield': 'm12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6z', 'settings': 'M9 3h6l1 4 4 2v6l-4 2-1 4H9l-1-4-4-2V9l4-2zM9 12a3 3 0 1 0 6 0a3 3 0 1 0-6 0', 'storage': 'M3 5h18v6H3zM3 15h18v6H3zM7 8h.01M7 18h.01', 'activity': 'M2 12h5l3-8 4 16 3-8h5', 'spark': 'm12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z', 'branch': 'M5 4v10h14m-5-5 5 5-5 5', 'download': 'M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4', 'plus': 'M12 5v14M5 12h14', 'circle': 'M16 12a4 4 0 1 0-8 0a4 4 0 1 0 8 0', 'help': 'M9 8a3 3 0 1 1 5 2c-2 1-2 2-2 4M12 18h.01'}

def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="{PATHS[name]}"/></svg>'
