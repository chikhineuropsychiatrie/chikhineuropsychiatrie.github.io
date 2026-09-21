// Videos : la vignette est remplacee par le lecteur YouTube (sans cookies) au clic.
// Sans JavaScript, ou en ctrl/cmd-clic, le lien ouvre simplement la video sur YouTube.
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a.video-facade');
  if (!a || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
  e.preventDefault();
  var f = document.createElement('iframe');
  f.className = 'video-frame';
  f.src = 'https://www.youtube-nocookie.com/embed/' + a.getAttribute('data-yt') + '?autoplay=1&rel=0';
  f.title = a.getAttribute('aria-label') || 'Vidéo';
  f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
  f.setAttribute('allowfullscreen', '');
  f.referrerPolicy = 'strict-origin-when-cross-origin';
  a.parentNode.replaceChild(f, a);
  f.focus();
});

// Menu mobile
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (!toggle || !nav) return;

  function setOpen(open) {
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  toggle.addEventListener('click', function () {
    setOpen(!nav.classList.contains('open'));
  });

  // Refermer au clic sur un lien, ou avec Echap
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      setOpen(false);
      toggle.focus();
    }
  });

  // Reinitialiser l'etat quand on repasse en affichage large
  var mq = window.matchMedia('(min-width: 901px)');
  var onChange = function (e) { if (e.matches) setOpen(false); };
  if (mq.addEventListener) mq.addEventListener('change', onChange);
  else if (mq.addListener) mq.addListener(onChange);
})();
