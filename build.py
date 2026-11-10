# -*- coding: utf-8 -*-
import json, os, shutil, html, datetime, zipfile

OUT = 'site'
SITE = 'https://espace-dentaire-malakoff.fr'
TODAY = '2026-11-09'
DOC = 'https://www.doctolib.fr/centre-dentaire/malakoff/espace-dentaire-malakoff/booking?bookingFunnelSource=external_referral&profile_skipped=true'
ORTHO = 'https://www.doctolib.fr/centre-dentaire/malakoff/espace-dentaire-malakoff/booking/motives?specialityId=270&telehealth=false&placeId=practice-207016&profile_skipped=true&bookingFunnelSource=external_referral'
E = lambda s: html.escape(s, quote=True)

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT + '/assets/img')
shutil.copy('src/style.css', OUT + '/assets/style.css')
shutil.copy('src/site.js', OUT + '/assets/site.js')
for n in ['accueil', 'cabinet', 'fauteuil', 'couloir', 'cabinet5', 'bloc']:
    shutil.copy(f'photos/{n}.jpg', f'{OUT}/assets/img/{n}.jpg')

pages = []      # (path, priority) pour le sitemap

def write(path, content):
    full = OUT + path
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)

# ---------------------------------------------------------------- logo
def logo(p):
    return f'''<svg class="logo" role="img" aria-label="Espace dentaire Malakoff" viewBox="0 0 220 112" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="{p}a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7FA3E6"/><stop offset="1" stop-color="#3C63B0"/></linearGradient>
<linearGradient id="{p}b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3C63B0"/><stop offset="1" stop-color="#1F3A6E"/></linearGradient></defs>
<path d="M2 52H86M134 52H218M2 84H218" stroke="#1F3A6E" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M110 12C98 0 80 4 80 20C80 34 88 40 91 56C92 63 99 64 101 56C103 48 106 44 110 42Z" fill="url(#{p}a)"/>
<path d="M110 12C122 0 140 4 140 20C140 34 132 40 129 56C128 63 121 64 119 56C117 48 114 44 110 42Z" fill="url(#{p}b)"/>
<path d="M110 12C106 22 106 34 110 42C114 34 114 22 110 12Z" fill="#0E1A38" fill-opacity=".5"/>
<g font-family="system-ui,-apple-system,Segoe UI,Roboto,sans-serif" font-weight="700" fill="#0E1A38">
<text x="2" y="75" font-size="14" letter-spacing="2.4">ESPACE</text>
<text x="218" y="75" font-size="13" letter-spacing="2.4" text-anchor="end">DENTAIRE</text>
<text x="2" y="106" font-size="17" textLength="216" lengthAdjust="spacing" fill="#1F3A6E">MALAKOFF</text></g>
</svg>'''

NAV = [('/', 'Accueil', 'home'), ('/c/lequipe-du-centre-dentaire/', 'L’équipe', 'equipe'),
       ('/c/les-soins-dentaires/', 'Soins dentaires', 'soins'), ('/c/orthodontie/', 'Orthodontie', 'ortho'),
       ('/c/contact/', 'Contact', 'contact')]

DENTIST_LD = {
    "@context": "https://schema.org", "@type": ["Dentist", "MedicalClinic"],
    "name": "Espace dentaire Malakoff", "url": SITE + "/", "telephone": "+33185626200",
    "image": SITE + "/assets/img/accueil.jpg",
    "address": {"@type": "PostalAddress", "streetAddress": "112 boulevard Gabriel Péri", "postalCode": "92240",
                "addressLocality": "Malakoff", "addressCountry": "FR"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "19:00"}],
    "medicalSpecialty": "Dentistry", "areaServed": "Malakoff",
    "sameAs": ["https://www.doctolib.fr/centre-dentaire/malakoff/espace-dentaire-malakoff"],
    "potentialAction": {"@type": "ReserveAction", "target": DOC, "name": "Prendre rendez-vous"}
}

def layout(path, title, desc, main, active=None, ld=None, noindex=False, og_type='website'):
    url = SITE + path
    cur = ' aria-current="page"'
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, cur if k == active else '', t) for h, t, k in NAV)
    ld_tags = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld or []))
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F5F7FB">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Espace dentaire Malakoff">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/accueil.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/style.css">
{ld_tags}</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="site-header"><div class="wrap">
<a href="/" aria-label="Espace dentaire Malakoff, accueil">{logo('h')}</a>
<nav class="nav" aria-label="Navigation principale">{nav}</nav>
<a class="btn btn-plein" href="{E(DOC)}">Prendre RDV</a>
</div></header>
<main id="contenu">
{main}
</main>
<footer class="site-footer">
<div class="wrap">
<div>{logo('f').replace('class="logo"', 'class="logo" style="width:150px;margin-bottom:16px"')}<p>Centre de santé dentaire à Malakoff (92240). Accepte les urgences dentaires.</p></div>
<div><h2>Rendez-vous</h2><p><a href="tel:+33185626200">01 85 62 62 00</a><br>Joignable 24h/24, 7j/7<br><a href="{E(DOC)}">Réserver sur Doctolib</a></p></div>
<div><h2>Horaires</h2><p>Lundi au vendredi<br>09:00–19:00</p></div>
<div><h2>Adresse</h2><p>112, Bd Gabriel Péri<br>92240 Malakoff</p></div>
</div>
<div class="copyright">
<a href="/c/honoraires/">Honoraires</a> · <a href="/c/infos-conseil-de-lordre/">Infos Conseil de l’Ordre</a> · <a href="/c/mentions-legales-espace-dentaire-malakoff-dentiste/">Mentions légales</a><br>
© {TODAY[:4]} Espace dentaire Malakoff
</div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''

def add(path, title, desc, main, active=None, ld=None, prio='0.6', **kw):
    write(path + 'index.html' if path.endswith('/') else path, layout(path, title, desc, main, active, ld, **kw))
    pages.append((path, prio))

def crumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
                                for i, (n, u) in enumerate(items)]}

def fil(items):
    out = []
    for i, (n, u) in enumerate(items):
        out.append(f'<a href="{u}">{E(n)}</a>' if i < len(items) - 1 else f'<span aria-current="page">{E(n)}</span>')
    return '<nav class="fil" aria-label="Fil d’Ariane">' + ' / '.join(out) + '</nav>'

PLAY = '<svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l13-7.5z" fill="#0A1020"/></svg>'

def videos_html(vids):
    out = []
    for vid, label in vids:
        out.append(f'<div><p class="legende">{E(label)}</p><div class="yt" data-yt="{vid}" data-titre="{E(label)}">'
                   f'<button type="button"><span class="play">{PLAY}</span>Lire la vidéo<small>Chargée depuis YouTube au clic</small></button>'
                   f'<noscript><a href="https://www.youtube.com/watch?v={vid}">Voir la vidéo sur YouTube</a></noscript></div></div>')
    return '<div class="videos">' + ''.join(out) + '</div>' if out else ''

def blocks_html(blocks):
    out = []
    first = True
    for b in blocks:
        if b.get('h'):
            out.append(f'<h2>{E(b["h"])}</h2>')
        if b.get('p'):
            cls = ' class="chapeau-article"' if first and not b.get('h') else ''
            out.append(f'<p{cls}>{E(b["p"])}</p>')
            first = False
        if b.get('items'):
            out.append('<ul>' + ''.join(f'<li>{E(i)}</li>' for i in b['items']) + '</ul>')
    return '\n'.join(out)

def first_text(blocks, n=155):
    for b in blocks:
        if b.get('p'):
            t = b['p']
            return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'
    return ''

def article(slug, title, blocks, vids, parent, related, cta='rdv', active='soins', desc=None, h1=None):
    path = f'/c/{slug}/'
    trail = [('Accueil', '/'), parent, (h1 or title, path)]
    rel = ''.join(f'<li><a href="/c/{s}/"><span>{E(t)}</span><span aria-hidden="true">›</span></a></li>' for s, t in related)
    btn = (f'<a class="btn btn-plein" href="{E(ORTHO)}">RDV orthodontie sur Doctolib</a>' if cta == 'ortho'
           else f'<a class="btn btn-plein" href="{E(DOC)}">Prendre RDV sur Doctolib</a>')
    main = f'''<div class="page-titre"><div class="wrap">
{fil(trail)}
<h1>{E(h1 or title)}</h1>
</div></div>
<section style="padding-top:32px"><div class="wrap"><div class="contenu">
{blocks_html(blocks)}
{videos_html(vids)}
<div class="cta-fin"><p>Une question sur ce sujet ? Le centre vous répond au 01 85 62 62 00, ou vous réservez en ligne à toute heure.</p><div class="row">{btn}<a class="btn btn-trait" href="tel:+33185626200">01 85 62 62 00</a></div></div>
<h2>À lire aussi</h2>
<ul class="liens-liste">{rel}</ul>
<p style="margin-top:36px"><a href="{parent[1]}">Retour : {E(parent[0])}</a></p>
</div></div></section>'''
    add(path, f'{title} à Malakoff (92240) | Espace dentaire Malakoff', desc or first_text(blocks), main, active,
        [crumb(trail)], prio='0.8', og_type='article')

# ---------------------------------------------------------------- soins (articles existants)
ARTS = {a['id']: a for a in json.load(open('data/arts.json', encoding='utf-8'))}
SOINS = [
    ('implants', 'les-implants-dentaires-expliques', 'Les implants dentaires expliqués', []),
    ('blanchiment', 'blanchiment-dentaire', 'Blanchiment dentaire', [('Y7BqI2_dnPY', 'Vidéo : le blanchiment dentaire')]),
    ('facettes', 'les-facettes-en-porcelaine-conventionnelles', 'Les facettes en porcelaine conventionnelles', [('vsDDYZ2kLi8', 'Vidéo : les facettes en porcelaine')]),
    ('hygiene', 'hygiene-dentaire', 'Hygiène dentaire', [('OesolCl2Vtk', 'Vidéo : l’hygiène dentaire'), ('_rPFOWAfeU0', 'Vidéo : la technique de brossage')]),
    ('caries', 'les-caries', 'Les caries', [('xvd_RKC7_Ko', 'Vidéo : les caries')]),
    ('endo', 'devitalisation-traitement-endodontique', 'Dévitalisation, traitement endodontique', [('BBIEeCoPcfg', 'Vidéo : la dévitalisation')]),
    ('protheses', 'les-protheses-et-bridges', 'Les prothèses et bridges', [('pbodn4iCLZg', 'Vidéo : le bridge dentaire'), ('_lkk3y4b7tU', 'Vidéo : la prothèse complète'), ('1RIoEUyh5T8', 'Vidéo : la prothèse complète, suite')]),
    ('paro', 'soins-des-gencives-parodontie', 'Soins des gencives, parodontie', [('OUYzTGtwecw', 'Vidéo : les soins des gencives')]),
    ('sagesse', 'dents-de-sagesse', 'Dents de sagesse', [('5JlDXDi8Vlw', 'Vidéo : les dents de sagesse')]),
    ('urgence', 'en-cas-durgence-dentaire', 'En cas d’urgence dentaire', []),
]
SOIN_INDEX = {s[0]: s for s in SOINS}
for i, (aid, slug, title, vids) in enumerate(SOINS):
    a = ARTS[aid]
    related = []
    for k in range(1, 4):
        o = SOINS[(i + k) % len(SOINS)]
        related.append((o[1], o[2]))
    article(slug, title, a['blocks'], vids, ('Soins dentaires', '/c/les-soins-dentaires/'), related,
            h1=('En cas d’urgence dentaire à Malakoff' if aid == 'urgence' else None),
            desc=None)

# ---------------------------------------------------------------- orthodontie
def P(t): return {'p': t}
def H(t, p=None, items=None):
    d = {'h': t}
    if p: d['p'] = p
    if items: d['items'] = items
    return d
ORTHO_PAGES = [
 ('le-principe-de-lorthodontie', 'Le principe de l’orthodontie', 'Principe de l’orthodontie', [
   P('L’orthodontie, partie de l’orthopédie dento-faciale, concerne plus particulièrement les malpositions des arcades et des dents.'),
   P('En empêchant l’apparition des malformations ou en les corrigeant, l’ODF permet non seulement de favoriser le bien-être social des patients, mais surtout de préserver la santé bucco-dentaire et donc la santé globale. Une fonction équilibrée et harmonieuse de l’appareil masticateur (articulations, muscles, dents) préserve sa santé et retarde les effets de son vieillissement naturel.'),
   P('L’ODF s’adresse aux enfants comme aux adultes, soit en première intention, soit associée à des traitements de prothèse ou à des traitements parodontaux (traitement des maladies des gencives responsables de la mobilité et du déplacement des dents).')],
   [('rdN05-frdNk', 'Vidéo : le principe de l’orthodontie')]),
 ('bilan-orthodontique', 'Bilan orthodontique', 'Bilan orthodontique', [
   P('Si un traitement orthodontique est envisagé, des examens complémentaires tels que des radiographies, des moulages en plâtre et parfois des photographies seront prescrits. Un bilan clinique précis, incluant des mesures et des constructions, sera réalisé pour proposer un plan de traitement adapté à la situation particulière du patient.'),
   P('À ce moment, le patient (et sa famille) seront informés du type d’appareil nécessaire (plusieurs appareils différents peuvent être nécessaires au cours d’une même phase de traitement) et de la durée prévisible du traitement ou de la phase de traitement concernée. Cette durée ne peut être qu’approximative : elle dépend de la coopération du patient, d’une réponse individuelle au traitement qui n’est jamais totalement identique et d’un degré d’incertitude sur la croissance faciale résiduelle ou la persistance d’une parafonction, comme la déglutition avec interposition de la langue.'),
   P('C’est à ce moment que sera recueilli le consentement éclairé, après avoir débattu de l’amélioration attendue, des contraintes et des risques éventuels du traitement ou de l’abstention de traitement.'),
   H('Les malformations les plus fréquentes sont dues à', items=[
     'La déformation des arcades dentaires, liée à la succion du pouce ou d’un autre doigt, à l’interposition de la langue pendant la déglutition, à la respiration par la bouche qui modifie la posture de la langue.',
     'Des dents trop grosses pour la taille de la bouche, ou inversement.',
     'Un décalage entre la croissance des deux mâchoires (squelettique).',
     'L’absence d’une ou de plusieurs dents (agénésie).',
     'Des dents incluses ou retenues dans la mâchoire.'])], []),
 ('depistage-en-orthodontie', 'Dépistage en orthodontie', 'Dépistage en orthodontie', [
   P('Un dépistage précoce est très important. Il n’existe pas d’âge standard pour débuter un traitement.'),
   P('Le praticien de l’art dentaire déterminera pour chaque situation le moment le plus propice pour débuter le traitement, en fonction de multiples paramètres. Ces paramètres sont liés à la génétique (croissance osseuse), à l’environnement (succion d’un doigt, respiration par la bouche, interposition de la langue pendant la déglutition…), au stade d’évolution de la denture (pas toujours en relation avec l’âge civil), à l’intensité ou à la gravité de la ou des déformations, et à l’association des différentes déformations (très fréquentes en orthodontie, car une déformation primaire induit des déformations secondaires). La maturité de l’enfant et sa capacité à coopérer devront aussi être prises en compte.'),
   P('Quelquefois, un traitement en deux étapes, séparées par une période de surveillance, sera indiqué : pour empêcher une aggravation chez un très jeune enfant, puis pour achever le traitement après l’évolution de toutes les dents permanentes.')], []),
 ('aligneurs-invisibles', 'Aligneurs invisibles', 'Orthodontie adulte, aligneurs invisibles', [
   P('Le système d’aligneurs invisibles est une technique qui a révolutionné l’orthodontie en corrigeant l’alignement des dents de façon quasi invisible et particulièrement confortable pour le patient.'),
   H('Le principe', 'Finis les bagues et autres fils métalliques en permanence dans la bouche ! L’originalité du système repose sur le port de gouttières transparentes appelées « aligneurs », fabriquées sur mesure pour chaque patient. L’aligneur provoque le déplacement de vos dents en exerçant une pression sur celles-ci. Ces déplacements sont prévus et calculés au millimètre (en réalité, moins que le millimètre !). À chaque rendez-vous, vous recevez une nouvelle gouttière d’alignement pour passer à l’étape suivante, jusqu’au résultat final où vos dents sont parfaitement alignées.'),
   H('La conception des aligneurs', 'Elle se fait grâce à la prise d’empreintes précise de vos dents et aux différentes informations que votre praticien recueille. Un logiciel enregistre l’ensemble des données et permet de visualiser en trois dimensions la position de vos dents à chaque étape. Votre praticien peut vous proposer un plan de traitement et vous montrer sur l’ordinateur le résultat du traitement avant de le commencer.'),
   H('La réalisation des aligneurs', 'Après avoir discuté du plan de traitement avec votre praticien et donné votre accord, les informations recueillies sont transmises à une société spécialisée. Celle-ci fabrique votre série d’aligneurs grâce à la conception assistée par ordinateur, puis les fait parvenir à votre praticien.'),
   H('Les avantages de l’orthodontie invisible', items=[
     'Le confort : au lieu de multi-attaches, de bagues et de fils métalliques souvent irritants pour la muqueuse, vous portez des gouttières que vous sentez à peine.',
     'La commodité : les aligneurs étant amovibles, ils peuvent être retirés à tout moment, en particulier lors des repas, pour le nettoyage, ou même avant un événement particulier. Ils doivent toutefois être portés un certain nombre d’heures par jour et par nuit pour être efficaces.',
     'L’esthétique : particulièrement fins et complètement transparents, les aligneurs sont quasiment invisibles.',
     'L’efficacité : les résultats sont remarquables et contrôlables chez votre dentiste à chaque étape grâce au logiciel de conception. Vous remarquez rapidement les premiers effets du traitement.']),
   P('Au bout du compte, avec tellement peu de contraintes, et après avoir obtenu le sourire de vos rêves, votre seul regret sera peut-être de ne pas avoir entrepris votre traitement orthodontique un peu plus tôt !')],
   [('_bsJ7fDZ0e4', 'Vidéo : les aligneurs invisibles')]),
 ('orthodontie-enfant', 'Orthodontie enfant', 'Orthodontie enfant', [
   P('En général, les enfants sont adressés à l’orthodontie à partir de 6 ans environ. C’est l’âge d’apparition de la première incisive et de la première molaire définitive.'),
   P('L’orthodontie, partie de l’orthopédie dento-faciale, concerne plus particulièrement les malpositions des arcades et des dents. En empêchant l’apparition des malformations ou en les corrigeant, l’ODF permet non seulement de favoriser le bien-être social des patients, mais surtout de préserver la santé bucco-dentaire et donc la santé globale. Une fonction équilibrée et harmonieuse de l’appareil masticateur préserve sa santé et retarde les effets de son vieillissement naturel.'),
   P('À cet âge, l’orthodontiste peut déjà plus ou moins prévoir l’évolution de la croissance des mâchoires (décalage entre le haut et le bas, par exemple), qui va déterminer le futur profil. Il existe des traitements dits interceptifs, qui permettent d’agir sur la croissance afin de la guider.'),
   P('Certains recommandent une première visite dès l’âge de 4 ans, en particulier en cas de respiration buccale ou d’habitudes déformantes (succion du pouce, par exemple). Votre orthodontiste dispose de différentes sortes d’appareillages pour traiter ces problèmes fonctionnels. Il peut aussi collaborer avec un orthophoniste quand une rééducation fonctionnelle est recommandée.'),
   P('L’objectif est de favoriser une croissance harmonieuse, d’empêcher une anomalie de se développer et de simplifier les traitements ultérieurs, voire de les rendre inutiles dans certains cas.'),
   P('C’est pourquoi, si vous remarquez chez votre enfant un défaut d’alignement des dents ou autre, ou si votre dentiste vous le conseille, il est conseillé de prendre rendez-vous pour une évaluation et un traitement adapté.')], []),
 ('esthetique-appareillage', 'Esthétique appareillage', 'Esthétique de l’appareillage', [
   H('Appareillages fixes multi-attaches', 'Les verrous esthétiques sont de plus en plus utilisés, même chez les enfants et les adolescents. Ils sont très peu visibles : les patients les acceptent d’autant mieux.'),
   P('L’objectif est clair : atteindre l’alignement parfait de la dentition. C’est donc un travail d’orfèvre, au millimètre près. Ainsi, en fin de traitement, on s’approche de l’idéal esthétique, mais aussi fonctionnel, en prenant en compte l’occlusion générale du patient.'),
   H('Quels patients sont concernés ?', 'Souvent, ce sont les chirurgiens-dentistes qui adressent leurs patients au spécialiste de l’orthodontie : avant de réaliser un travail prothétique, il convient parfois de réaligner les dents, afin d’optimiser l’esthétique du résultat.', items=[
     'Les patients qui souhaitent (re)trouver le sourire (problèmes d’alignement…) et qui nous consultent directement.',
     'Le déplacement des dents chez l’adulte : l’orthodontie est possible à tout âge. Le praticien évalue si le traitement sera supporté par le patient (os, gencive).'])], []),
 ('le-traitement-en-orthodontie', 'Le traitement en orthodontie', 'Le traitement en orthodontie', [
   P('Pour mener à bien son traitement, votre praticien pourra demander la collaboration d’autres professionnels de santé : pédiatres, médecins spécialistes ORL, chirurgiens maxillo-faciaux, chirurgiens-dentistes, médecins stomatologistes, orthophonistes, kinésithérapeutes…'),
   H('Les appareils les plus utilisés', items=[
     'Les appareils amovibles, que le patient peut retirer : ils comportent divers ressorts, vérins et positionneurs.',
     'Les appareils fixes, que le patient ne peut pas retirer : appareils métalliques, esthétiques en céramique (moins visibles), ou utilisés en technique linguale (totalement invisibles). Ils sont constitués de boîtiers ou verrous collés ou scellés sur les dents, reliés par des fils métalliques dont l’alliage, la section et la forme sont déterminés par les différentes étapes du traitement.',
     'Les appareils auxiliaires, utilisés avec les appareils fixes ou amovibles : élastiques, ancrage extra-oral (arc facial) ou bande de tissu péricrânien.',
     'Les traitements complémentaires : extractions dentaires, chirurgie buccale ou maxillo-faciale, traitements médicaux, ablation des végétations ou des amygdales, mini-vis, orthophonie…',
     'Les techniques collées : il existe diverses possibilités, externes et internes. Les brackets métalliques peuvent être remplacés, par souci d’esthétique, par des éléments transparents ou de la couleur des dents. Les techniques linguales offrent un appareil orthodontique efficace et totalement invisible.',
     'La contention : cette période correspond à la conservation du résultat obtenu. Le patient porte un appareil de nuit ou fait coller un fin fil à l’arrière des dents, pendant une durée plus ou moins longue selon la tendance à la récidive (retour à l’état antérieur), très variable selon les personnes et les malformations. Cette phase est trop souvent négligée par les patients ; elle est pourtant essentielle pour la pérennité du résultat. Le vieillissement de la denture s’accompagnant quelquefois de modifications de la position des dents, le patient doit rester vigilant et ne pas omettre les visites annuelles de contrôle chez son praticien traitant.'])], []),
 ('remboursement-mutuelle-et-securite-sociale', 'Remboursement mutuelle et Sécurité sociale', 'Remboursement mutuelle', [
   H('Avant 16 ans', 'Le traitement d’orthodontie est pris en charge par la Sécurité sociale si une demande d’entente préalable est faite avant le 16e anniversaire.'),
   H('Après 16 ans', 'Les traitements ne sont pas pris en charge par les caisses primaires d’assurance maladie (CPAM). Seules certaines mutuelles, selon les clauses du contrat, qui est personnel, assurent le remboursement, en totalité ou en partie, des traitements d’orthodontie.'),
   P('Toutefois, en cas de traitement après le 16e anniversaire associant chirurgie et orthodontie, un semestre de traitement peut éventuellement être pris en charge.'),
   P('Pour tout traitement, un devis est systématiquement remis afin que vous puissiez prendre contact avec les organismes concernés.')], []),
 ('age-de-traitement-orthodontique', 'Âge du traitement orthodontique', 'Âge du traitement', [
   P('Voici les principaux âges de traitement.'),
   H('Moins de 7 ans', 'Sucer le pouce, ventiler par la bouche, certains mouvements de la langue peuvent générer des malformations de la mâchoire et des dents. Le praticien pourra proposer un appareillage ou de la rééducation.'),
   H('8-11 ans', 'C’est au moment de la sortie des dents définitives que l’on s’aperçoit d’un éventuel chevauchement. À cet âge, il est possible d’accélérer ou de ralentir la croissance des mâchoires.'),
   H('Adolescent', 'À cause du manque de place ou de maxillaires décalés, la consultation est nécessaire. Parmi les plans de traitement, on envisage les extractions et, bien sûr, le réalignement des dents par la pose de bagues.'),
   H('Adulte', 'L’orthodontie concerne aussi les adultes. Les progrès techniques ont permis de proposer une orthodontie quasiment invisible. Pour plus d’informations, parlez-en au praticien.')], []),
 ('orthodontie-preventive', 'Orthodontie préventive', 'Orthodontie préventive', [
   H('À quel âge faut-il consulter ?', 'Mieux vaut prévenir que guérir : l’adage résume l’orthodontie préventive, aussi appelée interception.'),
   P('Le principe est simple : en intervenant tôt, les corrections seront bien plus simples. Dès l’âge de 4 ans, on peut observer la bouche de l’enfant et demander conseil à son dentiste ou à son praticien. De toute façon, un premier bilan est fortement recommandé avant l’âge de 8 ans.'),
   H('Le traitement', 'Suite au diagnostic, différents types de traitements pourront être proposés.')], []),
 ('systemes-multi-attaches', 'Systèmes multi-attaches', 'Systèmes multi-attaches', [
   H('Le système classique', 'Il y a quelques années, le seul système multi-attaches disponible en orthodontie était composé :', items=[
     'de brackets (ou attaches) en acier collés sur la partie visible de chaque dent ;',
     'de bagues scellées sur la dernière dent du fond, de chaque côté ;',
     'd’un arc dentaire qui parcourt l’ensemble bagues et brackets : c’est la torsion précise de cet arc au fil des séances qui provoque le déplacement des dents ;',
     'd’élastiques qui solidarisent chaque bracket à l’arc orthodontique.']),
   H('Les nouveaux systèmes multi-attaches', 'Ils ont été mis au point pour améliorer le confort, l’esthétique et l’efficacité des traitements orthodontiques. Aujourd’hui, on peut vous proposer par exemple :'),
   H('Les brackets transparents', 'Réalisés en céramique de grande qualité, ils se fondent littéralement avec la couleur de la dent et sont pratiquement invisibles. Leur teinte n’est pas altérée par la consommation d’aliments colorants (thé, café…). Ils conviennent aussi bien aux adultes qu’aux adolescents, et même aux enfants.'),
   H('Les appareils multi-attaches auto-ligaturants', 'Plus besoin de petits élastiques inconfortables, qui perdent leur couleur avec l’alimentation et retiennent la plaque dentaire : un élément solidaire du bracket clippe l’arc orthodontique, qui peut tout de même coulisser légèrement, ce qui favorise le déplacement des dents. Les brackets utilisés sont de taille réduite par rapport aux brackets classiques. Outre un avantage esthétique et une meilleure hygiène, ces appareils permettent une meilleure mobilisation des dents, ce qui réduit la longueur du traitement et le nombre de séances. Ce système convient aussi bien aux adultes qu’aux enfants.'),
   H('Les techniques linguales', 'Les brackets sont collés sur la face interne des dents. Plus petits que des brackets conventionnels, ils sont réalisés sur mesure grâce aux techniques de CAO (conception assistée par ordinateur), tout comme les arcs orthodontiques. C’est un système efficace et le plus esthétique qui soit en matière de multi-attaches, puisqu’il est totalement invisible. Il est réservé aux adultes et aux adolescents.'),
   P('Aujourd’hui, porter un appareil multi-attaches est devenu moins contraignant et plus esthétique, et les objectifs sont atteints plus rapidement qu’avec les systèmes classiques. Parlez-en avec votre orthodontiste : il saura vous conseiller le traitement le plus adapté à votre cas et à vos souhaits.')], []),
 ('la-contention', 'La contention', 'La contention', [
   P('Une contention orthodontique est un dispositif servant à maintenir dans le temps les résultats obtenus pendant la phase active du traitement orthodontique. Sans contention dentaire, on assiste à un déplacement spontané des dents une fois l’appareillage définitivement retiré. Généralement, les dents ont tendance à retourner à leur position initiale, mais on observe parfois l’apparition d’une nouvelle anomalie. La contention est donc indispensable pour éviter une récidive et s’assurer de la réussite du traitement.'),
   H('Quels systèmes de contention en orthodontie ?', 'Un appareil de contention est soit fixe, soit amovible, et la période pendant laquelle il est porté varie selon le cas. Voici les principaux types de contention orthodontique.'),
   H('Le fil de contention dentaire', 'Il s’agit d’un fil métallique rigide collé sur la face interne des dents de devant, de canine à canine. Particulièrement discret et facile à tolérer, il est souvent porté définitivement chez les adultes à la suite du traitement.'),
   H('Les gouttières orthodontiques', 'Une gouttière invisible est une excellente contention. Amovible, elle n’exerce pas de mobilisation des dents, mais maintient l’alignement obtenu par le traitement.'),
   H('La plaque palatine', 'C’est une contention amovible comprenant une plaque en résine qui s’appuie sur le palais et un fil métallique sur la face visible des incisives et canines du haut. Elle est réservée aux jeunes enfants et portée pendant une durée limitée.'),
   P('En cas de bris ou de perte de votre appareil de contention, il est impératif de prendre rapidement contact avec le cabinet afin qu’il puisse être remplacé ou réparé au plus vite.')], []),
 ('en-cas-durgence-en-orthodontie', 'En cas d’urgence en orthodontie', 'En cas d’urgence', [
   H('Service de garde', 'Le Conseil de l’Ordre départemental des chirurgiens-dentistes organise un service de garde pour les dimanches et jours fériés. Vous obtiendrez les coordonnées du dentiste de garde en téléphonant au commissariat ou à la gendarmerie de votre ville.'),
   P('En cas de traumatisme dentaire (suite à une chute, par exemple), nous vous invitons à prendre contact au plus tôt avec le cabinet par téléphone au 01 85 62 62 00, ou avec l’hôpital le plus proche (service d’odontologie ou de stomatologie et chirurgie maxillo-faciale).')],
   [('VogAleQAw8Q', 'Vidéo : que faire en cas d’urgence avec son appareil')]),
 ('trucs-et-astuces-en-orthodontie', 'Trucs et astuces en orthodontie', 'Trucs et astuces', [
   P('Voici quelques conseils fournis par la Fédération française d’orthodontie.')],
   [('VogAleQAw8Q', 'Conseils de la Fédération française d’orthodontie, 1'), ('v4BBFI7r7pk', 'Conseils de la Fédération française d’orthodontie, 2')]),
 ('brossage-des-dents-orthodontie', 'Brossage des dents en orthodontie', 'Brossage des dents', [
   P('Pendant le traitement orthodontique, le brossage des dents doit être particulièrement méticuleux.')],
   [('feyaEbdJgIU', 'Vidéo : le brossage des dents pendant le traitement orthodontique')]),
 ('orthodontie-linguale', 'Orthodontie linguale', 'Orthodontie linguale', [
   P('La technique d’orthodontie linguale utilise des appareils multi-attaches totalement invisibles, puisqu’ils sont placés sur la face interne (linguale) des dents. C’est donc le système le plus esthétique en matière de traitement orthodontique.'),
   H('La conception', 'Du fait de leur position, les attaches (ou brackets) doivent être conçues et réalisées sur mesure pour chaque patient, chaque bracket devant s’adapter parfaitement à la surface de la dent sur laquelle il sera collé. De la même manière, les fils métalliques (arcs orthodontiques) sont réalisés sur mesure pour un maximum de précision et d’efficacité.'),
   P('On utilise pour cela un logiciel spécifique. Les caractéristiques des dents (forme, surface, position…) et de la mâchoire sont enregistrées, et le traitement est réalisé de façon virtuelle sur l’ordinateur. À partir de ces données, les brackets ainsi que la série d’arcs orthodontiques sont fabriqués grâce à la technique de CAO, puis livrés à votre orthodontiste.'),
   P('La technique linguale permet de soigner la plupart des problèmes de malposition des dents, et ceci de façon totalement invisible pendant toute la durée du traitement orthodontique.')], []),
 ('videos-orthodontie', 'Vidéos orthodontie', 'Vidéos', [
   P('Une sélection de vidéos pédagogiques pour comprendre les principaux appareils et techniques d’orthodontie.')],
   [('Cvr_cpOOrvI', 'Le stripping'), ('rdN05-frdNk', 'Orthodontie'), ('Q8UQIpv8dwc', 'Orthodontie invisible'),
    ('UADZFGoTu-Q', 'Orthodontie Damon'), ('cIaDbUPnv8I', 'Élastiques'), ('HlTmbpznaSA', 'Quad hélix'),
    ('xQcc_x1Nba4', 'Plaque d’expansion'), ('_bsJ7fDZ0e4', 'Gouttières'), ('4HnLWog-TrY', 'Contention'),
    ('hX88qfd3MqQ', 'Lingual'), ('rjhyBeFioh4', 'Arc lingual'), ('gppj_CpVnuk', 'Préprothétique'),
    ('LNjM2v26T44', 'Réduction amélaire proximale'), ('ZjedOoW3SHA', 'PUL')]),
]
for i, (slug, title, label, blocks, vids) in enumerate(ORTHO_PAGES):
    related = [(ORTHO_PAGES[(i + k) % len(ORTHO_PAGES)][0], ORTHO_PAGES[(i + k) % len(ORTHO_PAGES)][1]) for k in (1, 2, 3)]
    article(slug, title, blocks, vids, ('Orthodontie', '/c/orthodontie/'), related, cta='ortho', active='ortho')

# ---------------------------------------------------------------- pages de liste
def cartes(items):
    return '<div class="grille">' + ''.join(
        f'<a class="carte" href="/c/{s}/"><h3>{E(t)}</h3><p>{E(d)}</p></a>' for s, t, d in items) + '</div>'

soin_desc = {
    'implants': 'Remplacer une dent manquante, sinus lift et greffe osseuse.',
    'blanchiment': 'Gouttières ou séances au cabinet.',
    'facettes': 'Corriger la couleur et la forme des dents de devant.',
    'hygiene': 'Brossage, brosse à dents, dentifrice.',
    'caries': 'Comprendre, prévenir et soigner.',
    'endo': 'Soigner l’intérieur de la dent.',
    'protheses': 'Couronnes, bridges, prothèses complètes.',
    'paro': 'Prévenir et traiter les maladies des gencives.',
    'sagesse': 'Quand les extraire, et pourquoi consulter.',
    'urgence': 'Que faire, et qui appeler.',
}
main = f'''<div class="page-titre"><div class="wrap">{fil([('Accueil', '/'), ('Soins dentaires', '/c/les-soins-dentaires/')])}
<h1>Les soins dentaires</h1>
<p style="max-width:640px;margin:20px 0 0;font-size:19px">Des fiches claires pour comprendre chaque soin avant votre rendez-vous.</p></div></div>
<section style="padding-top:40px"><div class="wrap">
{cartes([(s[1], s[2], soin_desc[s[0]]) for s in SOINS])}
<div class="cta-fin" style="max-width:760px"><p>Un soin ne figure pas dans la liste ? Le centre vous répond au 01 85 62 62 00.</p><div class="row"><a class="btn btn-plein" href="{E(DOC)}">Prendre RDV sur Doctolib</a></div></div>
</div></section>'''
add('/c/les-soins-dentaires/', 'Soins dentaires à Malakoff (92240) : implants, caries, gencives, blanchiment | Espace dentaire Malakoff',
    'Implants, blanchiment, facettes, caries, dévitalisation, prothèses, parodontie, dents de sagesse et urgences : toutes nos fiches de soins dentaires à Malakoff.',
    main, 'soins', [crumb([('Accueil', '/'), ('Soins dentaires', '/c/les-soins-dentaires/')])], prio='0.9')

ortho_cards = cartes([(s, l, '') for s, t, l, b, v in ORTHO_PAGES])
main = f'''<div class="page-titre"><div class="wrap">{fil([('Accueil', '/'), ('Orthodontie', '/c/orthodontie/')])}
<h1>Orthodontie à Malakoff</h1>
<p style="max-width:640px;margin:20px 0 0;font-size:19px">L’orthodontie s’adresse aux enfants comme aux adultes. Retrouvez ici toutes nos fiches d’information, et prenez rendez-vous directement avec l’orthodontiste du centre.</p>
<div class="row" style="margin-top:28px"><a class="btn btn-plein" href="{E(ORTHO)}">RDV orthodontie sur Doctolib</a><a class="btn btn-trait" href="tel:+33185626200">01 85 62 62 00</a></div></div></div>
<section style="padding-top:48px"><div class="wrap">{ortho_cards}</div></section>'''
add('/c/orthodontie/', 'Orthodontie à Malakoff (92240) : enfants, adultes, aligneurs invisibles | Espace dentaire Malakoff',
    'Orthodontie enfant et adulte à Malakoff : aligneurs invisibles, orthodontie linguale, multi-attaches, contention, remboursement. Prenez rendez-vous en ligne.',
    main, 'ortho', [crumb([('Accueil', '/'), ('Orthodontie', '/c/orthodontie/')])], prio='0.9')

# ---------------------------------------------------------------- équipe
TEAM = [('Dr Simon Atlan', 'Chirurgien-dentiste', 'SA', None), ('Dr Laura Benchetrit', 'Chirurgien-dentiste', 'LB', None),
        ('Dr Cyriele Berdah', 'Chirurgien-dentiste', 'CB', None), ('Dr Pierre-Alexandre Bouvet', 'Chirurgien-dentiste', 'PB', None),
        ('Dr Carla Levy', 'Orthodontie', 'CL', ORTHO), ('Dr Alicia Soussan', 'Référente du centre', 'AS', None),
        ('Christina', 'Assistante référente', 'C', None)]
cards = ''.join(f'<div class="membre"><div class="ini" aria-hidden="true">{i}</div><div><h3>{E(n)}</h3><p>{E(r)}</p></div>' +
                (f'<a href="{E(l)}">Prendre RDV en orthodontie</a>' if l else '') + '</div>' for n, r, i, l in TEAM)
main = f'''<div class="page-titre"><div class="wrap">{fil([('Accueil', '/'), ('L’équipe', '/c/lequipe-du-centre-dentaire/')])}
<h1>L’équipe du centre dentaire</h1></div></div>
<section style="padding-top:40px"><div class="wrap">
<div class="deux">
<div class="contenu">
<p class="chapeau-article">Au sein de l’Espace dentaire Malakoff, notre équipe de chirurgiens-dentistes vous accompagne pour l’ensemble de vos soins bucco-dentaires et de prévention.</p>
<p>Nos professionnels de l’art dentaire sont dûment diplômés et expérimentés. Leur présence au sein d’un même espace leur permet de mettre en commun leur savoir pour la résolution des cas les plus complexes de pathologie buccale ou de réhabilitation orale.</p>
<p>Nos chirurgiens-dentistes sont secondés par une équipe d’assistantes et de secrétaires efficaces, dévouées et… souriantes !</p>
<p>Tous sont soucieux d’établir une relation personnalisée et bienveillante avec chacun des patients que nous accueillons au 112, Bd Gabriel Péri, 92240 Malakoff.</p>
</div>
<img src="/assets/img/couloir.jpg" width="898" height="1600" alt="Couloir lumineux du centre dentaire" loading="lazy">
</div>
<div class="equipe">{cards}</div>
</div></section>'''
add('/c/lequipe-du-centre-dentaire/', 'L’équipe du centre dentaire de Malakoff (92240) | Espace dentaire Malakoff',
    'Chirurgiens-dentistes, orthodontiste, assistantes et secrétaires : découvrez l’équipe de l’Espace dentaire Malakoff.',
    main, 'equipe', [crumb([('Accueil', '/'), ('L’équipe', '/c/lequipe-du-centre-dentaire/')])], prio='0.7')

# ---------------------------------------------------------------- contact
main = f'''<div class="page-titre"><div class="wrap">{fil([('Accueil', '/'), ('Contact', '/c/contact/')])}
<h1>Contact et rendez-vous</h1></div></div>
<section style="padding-top:40px"><div class="wrap"><div class="grille">
<div class="carte"><h3>Téléphone</h3><p style="font-size:17px;color:var(--texte)">Joignable 24h/24, 7j/7 grâce à Recept AI.</p><a class="btn btn-plein" href="tel:+33185626200">01 85 62 62 00</a></div>
<div class="carte"><h3>En ligne</h3><p style="font-size:17px;color:var(--texte)">Prise de rendez-vous 24h/24 sur Doctolib.</p><div class="row"><a class="btn btn-plein" href="{E(DOC)}">RDV dentiste</a><a class="btn btn-trait" href="{E(ORTHO)}">RDV orthodontie</a></div></div>
<div class="carte"><h3>Horaires</h3><p style="font-size:17px;color:var(--texte)">Lundi au vendredi<br>09:00–19:00</p></div>
<div class="carte"><h3>Adresse</h3><p style="font-size:17px;color:var(--texte)">112, Bd Gabriel Péri<br>92240 Malakoff</p><a href="https://www.google.com/maps/search/?api=1&amp;query=112+Bd+Gabriel+P%C3%A9ri+92240+Malakoff" style="color:var(--ciel)">Itinéraire sur Google Maps</a></div>
</div></div></section>'''
add('/c/contact/', 'Contact et rendez-vous : dentiste à Malakoff (92240) | Espace dentaire Malakoff',
    'Contactez l’Espace dentaire Malakoff : 01 85 62 62 00, 112 boulevard Gabriel Péri, du lundi au vendredi de 9h à 19h. Rendez-vous en ligne 24h/24.',
    main, 'contact', [crumb([('Accueil', '/'), ('Contact', '/c/contact/')])], prio='0.8')

# ---------------------------------------------------------------- pages légales
def simple(slug, title, desc, body, h1=None, prio='0.3'):
    path = f'/c/{slug}/'
    main = f'''<div class="page-titre"><div class="wrap">{fil([('Accueil', '/'), (h1 or title, path)])}<h1>{E(h1 or title)}</h1></div></div>
<section style="padding-top:32px"><div class="wrap"><div class="contenu">{body}</div></div></section>'''
    add(path, f'{title} | Espace dentaire Malakoff', desc, main, None, [crumb([('Accueil', '/'), (h1 or title, path)])], prio=prio)

simple('honoraires', 'Honoraires, dentiste à Malakoff (92240)', 'Honoraires : actes conventionnés avec ou sans dépassement et actes hors nomenclature.', '''
<p>Les honoraires facturés dépendent du plan de traitement mis en œuvre et sont établis selon la typologie suivante :</p>
<h2>1. Les actes « conventionnés » sans dépassement</h2>
<p>Ce sont les actes de la nomenclature de la Sécurité sociale de type soins dentaires usuels (carie, détartrage…). La Sécurité sociale rembourse 60 % du tarif de convention dans la plupart des cas. Si vous disposez d’une mutuelle, elle vous remboursera le complément.</p>
<h2>2. Les actes « conventionnés » avec dépassement</h2>
<p>Afin de proposer une qualité irréprochable de service et une esthétique sans faille, le cabinet effectue des dépassements sur certains actes. Leur remboursement peut être pris en charge par votre mutuelle.</p>
<h2>3. Les actes « hors nomenclature »</h2>
<p>Ce sont les actes non pris en charge par la Sécurité sociale. Comme pour les dépassements d’honoraires, il convient de vous renseigner auprès de votre mutuelle afin d’en connaître le remboursement éventuel.</p>''', h1='Honoraires', prio='0.4')

simple('infos-conseil-de-lordre', 'Infos Conseil de l’Ordre', 'Charte ordinale de qualité applicable aux sites internet des chirurgiens-dentistes.', '''
<p>Les chirurgiens-dentistes sont des acteurs majeurs du secteur de la santé.</p>
<p>À ce titre, le Conseil national de l’Ordre des chirurgiens-dentistes a adopté une charte ordinale de « qualité », qui encadre la réalisation de sites internet dans la profession. Cette charte a pour but de faire respecter l’éthique et la déontologie de la profession.</p>
<p>Pour plus d’informations, vous pouvez accéder au site du <a href="https://www.ordre-chirurgiens-dentistes.fr/" rel="noopener">Conseil de l’Ordre</a>.</p>''', prio='0.3')

simple('mentions-legales-espace-dentaire-malakoff-dentiste', 'Mentions légales', 'Mentions légales du site de l’Espace dentaire Malakoff.', '''
<ul>
<li><strong>Responsable du site :</strong> Espace dentaire Malakoff</li>
<li><strong>SIRET :</strong> 899 203 004 00010</li>
<li><strong>Adresse :</strong> 112, Bd Gabriel Péri, 92240 Malakoff</li>
<li><strong>Téléphone :</strong> <a href="tel:+33185626200">01 85 62 62 00</a></li>
<li><strong>Hébergeur :</strong> [À COMPLÉTER : nom, adresse et contact de l’hébergeur choisi]</li>
</ul>
<p>Le responsable du site se porte garant du contenu rédactionnel du présent site.</p>
<h2>Traitement des données personnelles</h2>
<p>Ce site ne comporte aucun formulaire et ne collecte aucune donnée personnelle. La prise de rendez-vous se fait par téléphone ou sur le site de Doctolib, qui est responsable du traitement des données qu’il recueille.</p>
<p>Vous pouvez demander la correction ou l’effacement de vos données personnelles en contactant le responsable du site, en précisant « Traitement des données personnelles ».</p>
<h2>Cookies et vidéos</h2>
<p>Ce site n’utilise pas de cookies de suivi ni d’outil de mesure d’audience. Les vidéos YouTube ne sont chargées qu’après un clic de votre part, via le domaine youtube-nocookie.com ; YouTube peut alors déposer des cookies selon sa propre politique.</p>''', prio='0.2')

# ---------------------------------------------------------------- accueil
tick = ''.join(f'<span>{t}</span>' for t in ['Implants', 'Parodontie', 'Endodontie', 'Prothèses', 'Esthétique', 'Radiologie dentaire', 'Orthodontie', 'Urgences'])
home_cards = cartes([(s[1], s[2], soin_desc[s[0]]) for s in SOINS[:8]])
main = f'''<section class="hero"><div class="wrap">
<h1>Votre centre dentaire à Malakoff.</h1>
<p class="lead">Soins, implants, parodontie, endodontie, prothèses, orthodontie et urgences : tous vos soins dentaires réunis en un seul lieu, sur rendez-vous.</p>
<div class="row"><a class="btn btn-plein" href="{E(DOC)}">Réserver sur Doctolib</a><a class="btn btn-trait" href="tel:+33185626200">01 85 62 62 00</a></div>
<div class="infos"><span>Lundi au vendredi, 09:00–19:00</span><span>112 bd Gabriel Péri, 92240 Malakoff</span><span>Accepte les urgences</span></div>
</div></section>
<div class="bandeau" aria-label="Spécialités">{tick}</div>
<section><div class="wrap">
<div class="chapeau"><h2>Comprendre vos soins avant le rendez-vous</h2>
<p>Plus les consultations sont fréquentes, plus le coût des soins baisse. Pour garder vos dents toute la vie, une visite de contrôle au moins une fois par an est indispensable.</p></div>
{home_cards}
<p style="margin-top:28px"><a class="btn btn-trait" href="/c/les-soins-dentaires/">Tous les soins dentaires</a></p>
</div></section>
<section class="panneau"><div class="wrap">
<div class="permanence">
<div>
<span class="badge">24h/24 · 7j/7</span>
<h2>Joignable à toute heure, au téléphone.</h2>
<p>Grâce à Recept AI, un assistant vocal décroche vos appels de jour comme de nuit, 7 jours sur 7, et vous aide à prendre rendez-vous.</p>
<a class="btn btn-plein tel-grand" href="tel:+33185626200">01 85 62 62 00</a>
</div>
<div class="recept"><small>Propulsé par</small><strong>Recept<span> AI</span></strong><p>Secrétariat téléphonique par intelligence artificielle pour les cabinets de santé.</p></div>
</div></div></section>
<section class="fond-equipe"><div class="wrap"><div style="max-width:660px">
<h2>Une équipe, un seul lieu.</h2>
<p style="margin:18px 0 28px">Nos chirurgiens-dentistes vous accompagnent pour l’ensemble de vos soins bucco-dentaires et de prévention. Leur présence au sein d’un même espace leur permet de mettre en commun leur savoir pour les cas les plus complexes.</p>
<div class="row"><a class="btn btn-plein" href="/c/lequipe-du-centre-dentaire/">Découvrir l’équipe</a><a class="btn btn-trait" href="/c/orthodontie/">Orthodontie</a></div>
</div></div></section>
<section><div class="wrap"><div class="urgence">
<div><h2>Une urgence dentaire ?</h2><p>Le centre accepte les urgences. Le dimanche et les jours fériés, un service de garde est organisé par le Conseil de l’Ordre : demandez les coordonnées du dentiste de garde au commissariat ou à la gendarmerie de votre ville.</p></div>
<a class="btn" href="tel:+33185626200">01 85 62 62 00</a>
</div></div></section>'''
add('/', 'Dentiste à Malakoff (92240) | Espace dentaire Malakoff : implants, urgences, orthodontie',
    'Espace dentaire Malakoff : centre de santé dentaire au 112 bd Gabriel Péri. Soins, implants, parodontie, orthodontie, urgences. Rendez-vous en ligne 24h/24 ou au 01 85 62 62 00.',
    main, 'home', [DENTIST_LD], prio='1.0')

# ---------------------------------------------------------------- 404
write('/404.html', layout('/404.html', 'Page introuvable | Espace dentaire Malakoff', 'Page introuvable.',
    f'''<div class="page-titre"><div class="wrap"><h1>Page introuvable</h1>
<p style="margin:20px 0 28px;font-size:19px">Cette page n’existe pas ou a changé d’adresse. Retrouvez nos soins, ou appelez-nous au 01 85 62 62 00.</p>
<div class="row"><a class="btn btn-plein" href="/">Accueil</a><a class="btn btn-trait" href="/c/les-soins-dentaires/">Soins dentaires</a></div></div></div>''', noindex=True))

# ---------------------------------------------------------------- redirections des anciennes adresses
REDIR = {
    '/c/dentiste-malakoff-hauts-de-seine-92/': '/',
    '/node/9/': '/c/mentions-legales-espace-dentaire-malakoff-dentiste/',
    '/node/4/': '/c/contact/',
    '/c/videos-pedagogiques/': '/c/les-soins-dentaires/',
    '/c/videos-vos-dents-tout-age/': '/c/les-soins-dentaires/',
    '/c/implant-dentaire-video/': '/c/les-implants-dentaires-expliques/',
    '/node/63/': '/c/les-implants-dentaires-expliques/',
    '/node/64/': '/c/les-implants-dentaires-expliques/',
    '/node/65/': '/c/les-implants-dentaires-expliques/',
    '/c/parodontite-video/': '/c/soins-des-gencives-parodontie/',
    '/node/66/': '/c/soins-des-gencives-parodontie/',
    '/node/67/': '/c/soins-des-gencives-parodontie/',
    '/node/68/': '/c/soins-des-gencives-parodontie/',
    '/c/bridge-dentaire-video/': '/c/les-protheses-et-bridges/',
    '/c/inlay-onlay-esthetique-dentaire/': '/c/les-caries/',
    '/c/obturation-dentaire-video-plombage/': '/c/les-caries/',
}
for src, dst in REDIR.items():
    write(src + 'index.html', f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Redirection | Espace dentaire Malakoff</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{dst}">
<meta http-equiv="refresh" content="0; url={dst}"></head>
<body><p>Cette page a changé d’adresse : <a href="{dst}">continuer</a>.</p></body></html>
''')

# ---------------------------------------------------------------- fichiers techniques
write('/assets/favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1F3A6E"/><path d="M32 18C26 11 15 13 15 24C15 33 20 36 22 48C23 53 28 53 29 48C30 43 31 40 32 40C33 40 34 43 35 48C36 53 41 53 42 48C44 36 49 33 49 24C49 13 38 11 32 18Z" fill="#F5F7FB"/></svg>')
write('/CNAME', 'espace-dentaire-malakoff.fr\n')
write('/robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
urls = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p, pr in pages)
write('/sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
write('/LISEZMOI.txt', '''MISE EN LIGNE (GitHub Pages)
1. Créer un dépôt GitHub (ex. espace-dentaire-malakoff) et y déposer tout le contenu de ce dossier.
2. Settings > Pages : source = branche main, dossier racine.
3. Le fichier CNAME contient déjà le domaine espace-dentaire-malakoff.fr.
4. Chez le registrar du domaine : enregistrement A vers 185.199.108.153, .109.153, .110.153, .111.153 (et CNAME www vers <compte>.github.io).
5. Dans Settings > Pages : cocher « Enforce HTTPS ».
6. Compléter l'hébergeur dans la page Mentions légales (« À COMPLÉTER »).
7. Après mise en ligne : Google Search Console (envoyer sitemap.xml) et fiche Google Business.

Les anciennes adresses (/c/les-caries, etc.) sont conservées à l'identique.
''')
print(len(pages), 'pages indexables ;', len(REDIR), 'redirections')

