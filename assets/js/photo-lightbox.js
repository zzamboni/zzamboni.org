(() => {
  const dialog = document.querySelector('.photo-lightbox');
  if (!dialog) return;
  const image = dialog.querySelector('img');
  const counter = dialog.querySelector('[data-counter]');
  const previous = dialog.querySelector('[data-previous]');
  const next = dialog.querySelector('[data-next]');
  let photos = [], index = 0, origin, touch;
  function show(position) {
    index = (position + photos.length) % photos.length;
    image.src = photos[index].href;
    image.alt = photos[index].querySelector('img').alt;
    counter.textContent = `${index + 1} / ${photos.length}`;
    previous.hidden = next.hidden = photos.length < 2;
  }
  document.querySelectorAll('.photo-gallery').forEach(gallery => {
    const links = [...gallery.querySelectorAll('a')];
    links.forEach((link, position) => link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      photos = links;
      origin = link;
      show(position);
      dialog.showModal();
      document.documentElement.classList.add('photo-lightbox-open');
    }));
  });
  previous.addEventListener('click', () => show(index - 1));
  next.addEventListener('click', () => show(index + 1));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(index + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  image.addEventListener('touchstart', event => {
    touch = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  image.addEventListener('touchend', event => {
    if (!touch || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX - touch.x;
    const dy = event.changedTouches[0].clientY - touch.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(index + (dx < 0 ? 1 : -1));
    touch = null;
  }, { passive: true });
  image.addEventListener('touchcancel', () => { touch = null; });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('photo-lightbox-open');
    image.removeAttribute('src');
    origin?.focus();
  });
})();
