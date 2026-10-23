const search = document.querySelector('#search');
const niche = document.querySelector('#niche');
const cards = [...document.querySelectorAll('.book-card')];
function filterBooks() {
 const query = search.value.trim().toLowerCase();
 let shown = 0;
 for (const card of cards) {
  card.hidden = !(card.dataset.title.includes(query) && (niche.value === 'all' || card.dataset.niche === niche.value));
  if (!card.hidden) shown++;
 }
 document.querySelector('#count').textContent = `${shown} recommendation${shown === 1 ? '' : 's'}`;
 document.querySelector('#empty').hidden = shown > 0;
}
search.addEventListener('input', filterBooks);
niche.addEventListener('change', filterBooks);
