const f = document.getElementById('form');
const q = document.getElementById('query');

function submitted(event) {
    event.preventDefault();
    const win = window.open('https://www.google.com/', '_blank');
    win.focus();
  }
  
  f.addEventListener('submit', submitted);