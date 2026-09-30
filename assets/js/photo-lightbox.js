(() => {
  if (typeof GLightbox !== 'function') return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.photo-gallery').forEach(gallery => {
    const links = [...gallery.querySelectorAll('a')];
    if (!links.length) return;
    let origin, counter;
    const lightbox = GLightbox({
      selector: null,
      elements: links.map(link => ({
        href: link.href, type: 'image', alt: link.querySelector('img').alt
      })),
      loop: true,
      touchNavigation: true,
      keyboardNavigation: true,
      zoomable: true,
      draggable: true,
      preload: true,
      openEffect: reducedMotion ? 'none' : 'fade',
      closeEffect: reducedMotion ? 'none' : 'fade',
      slideEffect: reducedMotion ? 'none' : 'slide'
    });
    const updateCounter = () => {
      if (!counter) return;
      counter.textContent = `${lightbox.index + 1} / ${links.length}`;
    };
    lightbox.on('open', () => {
      const modal = lightbox.modal;
      modal.setAttribute('aria-label', gallery.dataset.label);
      modal.setAttribute('aria-modal', 'true');
      [['.gprev', 'previous'], ['.gnext', 'next'], ['.gclose', 'close']].forEach(([selector, label]) => {
        modal.querySelector(selector).setAttribute('aria-label', gallery.dataset[label]);
      });
      counter = document.createElement('span');
      counter.className = 'photo-lightbox-counter';
      counter.setAttribute('role', 'status');
      counter.setAttribute('aria-live', 'polite');
      modal.appendChild(counter);
      updateCounter();
      modal.querySelector('.gclose').focus();
      // Keep Tab and Shift-Tab inside the viewer, including single-photo galleries.
      modal.addEventListener('keydown', event => {
        if (event.key !== 'Tab') return;
        event.preventDefault();
        event.stopPropagation();
        const buttons = [...modal.querySelectorAll('.gbtn')].filter(button =>
          !button.classList.contains('disabled') && !button.classList.contains('glightbox-button-hidden'));
        const index = buttons.indexOf(document.activeElement);
        buttons[(index + (event.shiftKey ? -1 : 1) + buttons.length) % buttons.length].focus();
      });
    });
    lightbox.on('slide_changed', updateCounter);
    lightbox.on('close', () => origin?.focus({ preventScroll: true }));
    links.forEach((link, index) => link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      origin = link;
      lightbox.openAt(index);
    }));
  });
})();
