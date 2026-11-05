(() => {
  const cards = JSON.parse(document.getElementById('playcards-data').textContent);
  const en = document.documentElement.lang === 'en';
  const title = document.getElementById('card-title');
  const text = document.getElementById('card-text');
  const number = document.getElementById('card-number');
  const status = document.getElementById('cards-status');
  const previous = document.getElementById('previous-card');
  const card = document.querySelector('.playcard');
  let deck = [], history = [], position = -1;
  function render() {
    const item = cards[history[position]];
    title.textContent = item.title;
    text.textContent = item.text;
    const principle = document.getElementById('card-principle');
    principle.hidden = false;
    principle.textContent = item.principle;
    number.textContent = `${en ? 'PLAYCARD' : 'SPEELKAART'} / ${String(item.id).padStart(2, '0')}`;
    status.textContent = en ? `Card ${position + 1} drawn · ${cards.length} cards to explore` : `Kaart ${position + 1} getrokken · ${cards.length} kaarten om te ontdekken`;
    previous.disabled = position <= 0;
    card.classList.remove('is-new');
    void card.offsetWidth;
    card.classList.add('is-new');
  }
  document.getElementById('draw-card').addEventListener('click', () => {
    if (position < history.length - 1) { position++; render(); return; }
    if (!deck.length) {
      deck = cards.map((_, i) => i);
      for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
      }
      if (deck[deck.length - 1] === history[position]) [deck[0], deck[deck.length - 1]] = [deck[deck.length - 1], deck[0]];
    }
    history.push(deck.pop()); position++; render();
  });
  previous.addEventListener('click', () => { if (position > 0) { position--; render(); } });
})();
