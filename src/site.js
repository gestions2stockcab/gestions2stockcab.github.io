(function () {
  'use strict';

  /* ---------- Vidéos YouTube : chargées seulement au clic ---------- */
  document.querySelectorAll('.yt[data-yt]').forEach(function (box) {
    var btn = box.querySelector('button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + box.getAttribute('data-yt') + '?rel=0&autoplay=1';
      f.title = box.getAttribute('data-titre') || 'Vidéo';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      box.replaceChildren(f);
    });
  });

  /* ---------- Assistant d'orientation (sans serveur, sans collecte) ---------- */
  var DOC = 'https://www.doctolib.fr/centre-dentaire/malakoff/espace-dentaire-malakoff/booking?bookingFunnelSource=external_referral&profile_skipped=true';
  var ORTHO = 'https://www.doctolib.fr/centre-dentaire/malakoff/espace-dentaire-malakoff/booking/motives?specialityId=270&telehealth=false&placeId=practice-207016&profile_skipped=true&bookingFunnelSource=external_referral';
  var ACTIONS = {
    rdv: { t: 'Prendre RDV sur Doctolib', h: DOC },
    ortho: { t: 'RDV orthodontie sur Doctolib', h: ORTHO },
    urgence: { t: 'Appeler le 01 85 62 62 00', h: 'tel:+33185626200' }
  };

  function reply(text) {
    var s = text.toLowerCase();
    function has() { for (var i = 0; i < arguments.length; i++) { if (s.indexOf(arguments[i]) > -1) return true; } return false; }
    if (has('urgence', 'douleur', 'mal aux', 'mal à', 'saigne', 'gonfl', 'trauma', 'cassé', 'cassée', 'abcès', 'abces', 'chute'))
      return ['Le centre accepte les urgences : appelez-nous au plus tôt au 01 85 62 62 00. Les dimanches et jours fériés, les coordonnées du dentiste de garde s’obtiennent auprès du commissariat ou de la gendarmerie.', 'urgence'];
    if (has('ortho', 'appareil', 'bague', 'alignement', 'aligneur'))
      return ['Nous avons une orthodontiste au centre, le Dr Carla Levy. Vous pouvez prendre rendez-vous directement en orthodontie.', 'ortho'];
    if (has('implant', 'sinus', 'greffe osseuse'))
      return ['L’implant remplace une dent manquante sans toucher aux dents voisines. Nous réalisons aussi les greffes de sinus et d’os quand le volume osseux est insuffisant. Un rendez-vous permet de faire le point.', 'rdv'];
    if (has('blanch', 'facette', 'esthétique', 'esthetique', 'sourire'))
      return ['Pour l’esthétique du sourire, nous proposons le blanchiment (gouttières ou séances au cabinet) et les facettes en porcelaine. Le praticien commence par un bilan bucco-dentaire.', 'rdv'];
    if (has('carie', 'dévital', 'devital', 'plombage', 'obturation'))
      return ['Une carie se soigne d’autant plus simplement qu’elle est traitée tôt. N’attendez pas d’avoir mal : un contrôle permet de choisir le soin adapté.', 'rdv'];
    if (has('gencive', 'paro', 'déchauss', 'dechauss', 'tartre'))
      return ['Des gencives qui saignent, gonflent ou font mal sont un signe à ne pas négliger : consultez rapidement. Nous prenons en charge les maladies des gencives.', 'rdv'];
    if (has('couronne', 'bridge', 'prothèse', 'prothese', 'dentier'))
      return ['Couronnes, bridges, prothèses complètes (éventuellement stabilisées sur implants) : le praticien vous explique la solution la plus adaptée lors d’un rendez-vous.', 'rdv'];
    if (has('sagesse'))
      return ['L’extraction des dents de sagesse est souvent conseillée quand il manque de place dans la mâchoire. Il est utile de consulter pour prévenir les déplacements de dents.', 'rdv'];
    if (has('horaire', 'ouvert', 'ouverture', 'heure'))
      return ['Le centre est ouvert du lundi au vendredi, de 9h à 19h. La prise de rendez-vous en ligne est possible 24h/24 sur Doctolib, et notre assistant vocal décroche vos appels à toute heure.', 'rdv'];
    if (has('adresse', 'où', 'ou est', 'situé', 'accès', 'acces'))
      return ['Nous sommes au 112, boulevard Gabriel Péri, 92240 Malakoff.', 'rdv'];
    if (has('prix', 'tarif', 'honoraire', 'coût', 'cout', 'rembours'))
      return ['Les honoraires sont détaillés sur la page « Honoraires » du site, et l’équipe vous renseigne volontiers au 01 85 62 62 00.', 'rdv'];
    if (has('rdv', 'rendez', 'réserv', 'reserv', 'consult'))
      return ['Avec plaisir : vous pouvez réserver en ligne, 24h/24, sur Doctolib.', 'rdv'];
    return ['Je n’ai pas bien compris. Pouvez-vous préciser : une douleur, un soin précis (implant, blanchiment, orthodontie…) ou un simple contrôle ? Vous pouvez aussi réserver directement.', 'rdv'];
  }

  var open = document.createElement('button');
  open.className = 'chat-ouvrir';
  open.type = 'button';
  open.textContent = 'Une question ?';
  open.setAttribute('aria-haspopup', 'dialog');

  var box = document.createElement('div');
  box.className = 'chat';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-label', 'Assistant du centre');
  box.innerHTML =
    '<header><span>Assistant du centre</span><button type="button" aria-label="Fermer">×</button></header>' +
    '<div class="msgs" aria-live="polite"></div>' +
    '<div class="puces"></div>' +
    '<p class="avis">Cet assistant ne remplace pas un avis médical. En cas de douleur vive, de gonflement ou de traumatisme, appelez le 01 85 62 62 00.</p>' +
    '<form><input type="text" aria-label="Votre message" placeholder="Écrivez votre message…" autocomplete="off"><button type="submit" aria-label="Envoyer">→</button></form>';

  var msgs = box.querySelector('.msgs');
  var puces = box.querySelector('.puces');
  var input = box.querySelector('input');

  function add(cls, text) {
    var d = document.createElement('div');
    d.className = 'm ' + cls;
    d.textContent = text;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
  }
  function act(key) {
    var a = ACTIONS[key];
    if (!a) return;
    var l = document.createElement('a');
    l.className = 'act';
    l.href = a.h;
    l.textContent = a.t;
    msgs.appendChild(l);
    msgs.scrollTop = msgs.scrollHeight;
  }
  function send(text) {
    text = (text || '').trim();
    if (!text) return;
    add('moi', text);
    var r = reply(text);
    add('bot', r[0]);
    act(r[1]);
  }

  add('bot', 'Bonjour, je suis l’assistant de l’Espace dentaire Malakoff. Dites-moi ce qui vous amène : je vous oriente vers le bon soin et la prise de rendez-vous.');
  ['J’ai mal aux dents', 'Prendre rendez-vous', 'Implants', 'Orthodontie', 'Horaires'].forEach(function (label) {
    var b = document.createElement('button');
    b.type = 'button';
    b.textContent = label;
    b.addEventListener('click', function () { send(label); });
    puces.appendChild(b);
  });

  box.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    send(input.value);
    input.value = '';
  });
  function close() { box.classList.remove('ouvert'); open.style.display = ''; open.focus(); }
  box.querySelector('header button').addEventListener('click', close);
  box.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  open.addEventListener('click', function () { box.classList.add('ouvert'); open.style.display = 'none'; input.focus(); });

  document.body.appendChild(box);
  document.body.appendChild(open);
})();
