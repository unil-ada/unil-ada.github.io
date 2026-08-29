/* Course site liveness: date-aware status strip + expandable schedule rows.
   No dependencies. Reveal state (greying/links) stays static in HTML;
   time state (current/next session) is computed here. */
(function () {
  var qs = new URLSearchParams(location.search);
  var today = qs.get('today') ? new Date(qs.get('today') + 'T12:00:00') : new Date();
  today.setHours(12, 0, 0, 0);

  var rows = Array.prototype.slice.call(document.querySelectorAll('tr.session[data-date]'));
  var sessions = rows.map(function (tr) {
    return { tr: tr, date: new Date(tr.getAttribute('data-date') + 'T12:00:00'),
             title: (tr.querySelector('.q') || {}).firstChild ? tr.querySelector('.q').firstChild.textContent.trim() : '',
             skip: tr.hasAttribute('data-skip') };
  });
  var teaching = sessions.filter(function (s) { return !s.skip; });

  /* ---- which session is current / next ---- */
  var DAY = 86400000;
  var fmt = function (d) { return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }); };
  var current = null, next = null, idx = 0;
  for (var i = 0; i < teaching.length; i++) {
    if (teaching[i].date <= today) { current = teaching[i]; idx = i + 1; }
    else { next = teaching[i]; break; }
  }
  rows.forEach(function (tr) { tr.classList.remove('now'); });
  if (current) current.tr.classList.add('now');

  /* ---- status strip in the masthead ---- */
  var mast = document.querySelector('.mast .wrap');
  if (mast && teaching.length) {
    var total = teaching.length, pct = Math.round(100 * idx / total);
    var msg, sub;
    if (!current) {
      var days = Math.round((teaching[0].date - today) / DAY);
      msg = 'Semester starts in ' + days + (days === 1 ? ' day' : ' days');
      sub = 'First session: ' + fmt(teaching[0].date) + ' — ' + teaching[0].title;
    } else if (next) {
      var dn = Math.round((next.date - today) / DAY);
      msg = 'Session ' + idx + ' of ' + total;
      sub = 'Next: ' + fmt(next.date) + ' — ' + next.title + (dn === 0 ? ' — today' : ' — in ' + dn + (dn === 1 ? ' day' : ' days'));
    } else { msg = 'All ' + total + ' sessions taught'; sub = 'Thank you — see the exam session dates in Assessment.'; }
    var strip = document.createElement('div');
    strip.className = 'pulse';
    strip.innerHTML = '<div class="pulse-row"><b>' + msg + '</b><span>' + sub + '</span></div>' +
                      '<div class="bar"><div class="fill" style="width:' + pct + '%"></div></div>';
    mast.appendChild(strip);
  }

  /* ---- expandable rows ---- */
  rows.forEach(function (tr) {
    var detail = tr.nextElementSibling;
    if (!detail || !detail.classList.contains('detail')) return;
    tr.classList.add('expandable'); tr.setAttribute('tabindex', '0'); tr.setAttribute('role', 'button');
    tr.setAttribute('aria-expanded', 'false');
    var mat = tr.querySelector('.mat'), slot = detail.querySelector('.d-mat');
    if (mat && slot) slot.innerHTML = mat.innerHTML;   /* single source for links */
    var toggle = function () {
      var open = tr.classList.toggle('open');
      tr.setAttribute('aria-expanded', open ? 'true' : 'false');
      detail.classList.toggle('open', open);
    };
    tr.addEventListener('click', function (e) { if (e.target.closest('a')) return; toggle(); });
    tr.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } });
    if (tr.classList.contains('now')) toggle();          /* today's session opens by itself */
  });
})();
