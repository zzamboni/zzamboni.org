// Retain the instance so the article lightbox can detach images it takes over.
window.siteImageZoom = mediumZoom(document.querySelectorAll('img:not(.nozoom)'), {
  margin: 24,
  background: 'rgba(0,0,0,0.5)',
  scrollOffset: 0,
});
