// The floating header is viewport-fixed; keep its offset in sync when the
// notice wraps, fonts load, the viewport changes size, or it scrolls out of view.
(() => {
  const banner = document.querySelector('.deployment-banner');
  if (!banner) return;

  const updateHeight = () => {
    document.documentElement.style.setProperty(
      '--deployment-banner-height',
      `${Math.max(0, banner.getBoundingClientRect().bottom)}px`,
    );
  };

  updateHeight();
  new ResizeObserver(updateHeight).observe(banner);
  window.addEventListener('scroll', updateHeight, { passive: true });
})();
