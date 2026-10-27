(() => {
  if (typeof GLightbox !== 'function') return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.photo-gallery, .lightbox-gallery').forEach(gallery => {
    if (gallery.classList.contains('lightbox-gallery')) {
      gallery.querySelectorAll('figure').forEach(figure => {
        const img = figure.querySelector('img');
        if (!img) return;
        img.classList.add('nozoom');
        if (img.closest('a')) return;
        const link = document.createElement('a');
        link.href = img.dataset.zoomSrc || img.currentSrc || img.src;
        img.parentNode.insertBefore(link, img);
        link.appendChild(img);
      });
    }
    const links = [...gallery.querySelectorAll('figure a')].filter(link => link.querySelector('img'));
    if (gallery.classList.contains('lightbox-gallery')) {
      links.forEach(link => {
        const img = link.querySelector('img');
        link.href = img.dataset.zoomSrc || link.href;
        link.removeAttribute('target');
      });
    }
    if (!links.length) return;
    let origin, counter;
    const lightbox = GLightbox({
      selector: null,
      elements: links.map(link => {
        const caption = link.closest('figure')?.querySelector('figcaption');
        return {
          href: link.href, type: 'image', alt: link.querySelector('img').alt,
          // Reuse rendered caption markup; alt text is not a visible caption.
          description: caption?.textContent.trim() ? caption.innerHTML : ''
        };
      }),
      descPosition: 'bottom',
      moreLength: 0,
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
      counter.classList.toggle('has-caption', Boolean(
        lightbox.getActiveSlide()?.querySelector('.gslide-description')));
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
      // Include caption links, but never focus controls in inactive slides.
      modal.addEventListener('keydown', event => {
        if (event.key !== 'Tab') return;
        event.preventDefault();
        event.stopPropagation();
        const buttons = [...modal.querySelectorAll('.gbtn, .gslide.current .gslide-desc a[href]')].filter(button =>
          !button.classList.contains('disabled') && !button.classList.contains('glightbox-button-hidden') &&
          button.getClientRects().length > 0);
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
