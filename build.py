#!/usr/bin/env python3
"""
Watchmans Global — multi-page SEO build.

Generates:
  index.html              (landing: hero, cinema, ethos, enquire)
  collection.html         (full grid + multi-image gallery)
  bespoke-sourcing.html   (clientele, authentication, discretion)
  process.html            (6-step process + assurances)
  enquire.html            (contact methods + form)
  robots.txt
  sitemap.xml

Also copies logo.png to outputs so every page can reference it externally
(massive page-weight improvement vs. inline base64).
"""

import os, json, shutil

# ============================================================
# SITE CONSTANTS
# ============================================================
SITE_URL = "https://watchmansglobal.com"  # ← change to your real domain
PHONE = "+44 7932 026959"
PHONE_INTL = "+447932026959"
EMAIL = "info@watchmansglobal.com"
WHATSAPP = f"https://wa.me/{PHONE_INTL.lstrip('+')}"
INSTAGRAM = "https://instagram.com/watchmansglobal"
INSTAGRAM_HANDLE = "@watchmansglobal"
BRAND = "Watchmans Global"
TAGLINE = "Your Private Watch Concierge"
WEB3FORMS_KEY = "4abf5952-52c3-49fa-8d65-b5b287e72699"  # public access key — safe in client code

OUTDIR = "/mnt/user-data/outputs"
LOGO_SRC = "/home/claude/logo.png"


# ============================================================
# SHARED CSS — used on every page
# ============================================================
SHARED_CSS = r"""
  :root{
    --paper:#F4F0E8;--paper-2:#EDE7DA;--ink:#1A1714;--ink-soft:#615A4E;
    --line:#CFC6B4;--bronze:#9A7B4F;--bronze-deep:#7C5F38;--dark:#141310;
    --dark-soft:#9C9484;--serif:"Fraunces",Georgia,serif;
    --sans:"Hanken Grotesk",-apple-system,BlinkMacSystemFont,sans-serif;--maxw:1240px;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{background:var(--paper);color:var(--ink);font-family:var(--sans);
    font-weight:300;line-height:1.65;-webkit-font-smoothing:antialiased;
    font-size:17px;overflow-x:hidden}
  h1,h2,h3,h4{font-family:var(--serif);font-weight:300;line-height:1.08;letter-spacing:-0.01em}
  a{color:inherit;text-decoration:none}
  img{max-width:100%;display:block}
  .wrap{max-width:var(--maxw);margin:0 auto;padding:0 40px}
  .eyebrow{font-size:11.5px;letter-spacing:.28em;text-transform:uppercase;
    font-weight:500;color:var(--bronze-deep)}
  .btn{display:inline-block;font-family:var(--sans);font-size:12.5px;
    letter-spacing:.22em;text-transform:uppercase;font-weight:500;
    padding:17px 38px;border:1px solid var(--ink);background:var(--ink);
    color:var(--paper);cursor:pointer;transition:.45s ease}
  .btn:hover{background:transparent;color:var(--ink)}
  .btn.ghost{background:transparent;color:var(--ink)}
  .btn.ghost:hover{background:var(--ink);color:var(--paper)}
  .btn.light{border-color:var(--paper);background:transparent;color:var(--paper)}
  .btn.light:hover{background:var(--paper);color:var(--dark)}
  /* HEADER */
  header{position:fixed;top:0;left:0;right:0;z-index:100;transition:.5s ease;
    border-bottom:1px solid transparent}
  header.scrolled,header.solid{background:rgba(244,240,232,.92);backdrop-filter:blur(12px);
    border-bottom:1px solid var(--line)}
  nav{display:flex;align-items:center;justify-content:space-between;height:84px;
    max-width:var(--maxw);margin:0 auto;padding:0 40px}
  .logo-img{height:28px;width:auto;cursor:pointer}
  .navlinks{display:flex;gap:42px;align-items:center}
  .navlinks a{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;
    font-weight:400;color:var(--ink-soft);transition:.3s;position:relative}
  .navlinks a:hover{color:var(--ink)}
  .navlinks a.on{color:var(--ink)}
  .navlinks a.on::after{content:"";position:absolute;left:0;right:0;bottom:-8px;
    height:1px;background:var(--bronze)}
  .navlinks a.cta{color:var(--ink);border:1px solid var(--line);
    padding:11px 22px;letter-spacing:.18em}
  .navlinks a.cta:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
  .navlinks a.cta.on::after{display:none}
  .burger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:0;
    width:36px;height:36px;align-items:center;justify-content:center;z-index:110;position:relative}
  .burger span{width:22px;height:1.5px;background:var(--ink);transition:.3s}
  .burger.open span:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
  .burger.open span:nth-child(2){opacity:0}
  .burger.open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
  /* SECTIONS */
  section{position:relative}
  main{display:block}
  .pad{padding:130px 0}
  .reveal{opacity:0;transform:translateY(34px);transition:1s cubic-bezier(.16,1,.3,1)}
  .reveal.in{opacity:1;transform:none}
  .grain{position:absolute;inset:0;opacity:.4;pointer-events:none;z-index:1;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.3'/%3E%3C/svg%3E")}
  /* PAGE HERO (interior pages) */
  .page-hero{padding:170px 0 80px;position:relative;overflow:hidden;
    background:radial-gradient(900px 600px at 78% 14%,rgba(154,123,79,.14),transparent 60%),
      radial-gradient(700px 500px at 12% 92%,rgba(20,19,16,.05),transparent 55%),var(--paper)}
  .page-hero .wrap{position:relative;z-index:2}
  .page-hero .eyebrow{margin-bottom:30px;display:inline-block}
  .page-hero h1{font-size:clamp(48px,7vw,96px);letter-spacing:-0.025em;
    margin-bottom:32px;max-width:920px;line-height:1.04}
  .page-hero h1 em{font-style:italic;color:var(--bronze)}
  .page-hero .lead{font-size:19px;color:var(--ink-soft);max-width:600px;line-height:1.65}
  /* MARQUEE */
  .marquee{border-top:1px solid var(--line);border-bottom:1px solid var(--line);
    padding:26px 0;overflow:hidden;background:var(--paper-2)}
  .marquee-track{display:flex;gap:70px;white-space:nowrap;
    animation:slide 38s linear infinite;width:max-content}
  .marquee-track span{font-family:var(--serif);font-size:21px;font-style:italic;
    color:var(--ink-soft);display:flex;align-items:center;gap:70px}
  .marquee-track span::after{content:"·";color:var(--bronze)}
  @keyframes slide{to{transform:translateX(-50%)}}
  /* ENQUIRE SECTION (appears on every page bottom) */
  .enquire{background:var(--paper-2);padding:120px 0;border-top:1px solid var(--line)}
  .enq-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:80px;align-items:start}
  .enq-grid h2{font-size:clamp(34px,4.4vw,56px);margin-bottom:24px}
  .enq-grid h2 em{font-style:italic;color:var(--bronze)}
  .enq-grid .enq-lead{font-size:17px;color:var(--ink-soft);line-height:1.7;margin-bottom:32px}
  .enq-contacts{display:flex;flex-direction:column;gap:14px;margin-top:38px;
    padding-top:32px;border-top:1px solid var(--line)}
  .enq-contacts a{display:flex;align-items:center;gap:14px;font-size:15px;
    color:var(--ink-soft);transition:.3s;padding:8px 0}
  .enq-contacts a:hover{color:var(--bronze-deep)}
  .enq-contacts a b{font-family:var(--serif);font-style:italic;color:var(--ink);
    font-weight:300;font-size:16px;min-width:120px;display:inline-block}
  .enq-form{background:var(--paper);border:1px solid var(--line);padding:46px 44px}
  .enq-form h3{font-size:24px;margin-bottom:6px}
  .enq-form .form-sub{font-size:13.5px;color:var(--ink-soft);
    letter-spacing:.04em;margin-bottom:32px}
  .enq-form .form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}
  .enq-form label{display:block}
  .enq-form .lbl{font-size:11px;letter-spacing:.18em;text-transform:uppercase;
    color:var(--bronze-deep);font-weight:600;margin-bottom:8px}
  .enq-form input,.enq-form textarea,.enq-form select{width:100%;
    font-family:var(--sans);font-size:14.5px;color:var(--ink);
    background:var(--paper);border:1px solid var(--line);padding:14px 16px;
    transition:.3s;font-weight:300}
  .enq-form input:focus,.enq-form textarea:focus,.enq-form select:focus{
    outline:0;border-color:var(--ink)}
  .enq-form textarea{min-height:120px;resize:vertical;font-family:var(--sans)}
  .enq-form .form-foot{display:flex;justify-content:space-between;
    align-items:center;margin-top:24px;flex-wrap:wrap;gap:16px}
  .enq-form .form-fine{font-size:12px;color:var(--ink-soft);letter-spacing:.02em;
    max-width:280px}
  .form-status{margin-top:18px;font-size:14px;padding:14px 16px;display:none}
  .form-status.ok{display:block;background:rgba(154,123,79,.1);
    border:1px solid var(--bronze);color:var(--bronze-deep)}
  .form-status.err{display:block;background:rgba(200,80,80,.08);
    border:1px solid #c85050;color:#9a4040}
  /* FOOTER */
  footer{background:var(--paper);padding:80px 0 50px;border-top:1px solid var(--line)}
  .foot-top{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:50px;
    padding-bottom:60px;border-bottom:1px solid var(--line)}
  .foot-logo{height:30px;margin-bottom:22px}
  .foot-top p{font-size:14px;color:var(--ink-soft);max-width:270px}
  .fcol h5{font-size:11px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--bronze-deep);margin-bottom:22px;font-weight:600}
  .fcol a{display:block;font-size:14.5px;color:var(--ink-soft);margin-bottom:13px;
    transition:.3s;cursor:pointer}
  .fcol a:hover{color:var(--ink)}
  .foot-bot{display:flex;justify-content:space-between;padding-top:34px;
    font-size:12.5px;color:var(--ink-soft);letter-spacing:.04em;flex-wrap:wrap;gap:12px}
  /* LEGAL OVERLAY (privacy / terms / authenticity) */
  .legal-screen{display:none;position:fixed;inset:0;z-index:200;
    overflow-y:auto;background:var(--paper);color:var(--ink)}
  .legal-screen.active{display:block}
  body.locked{overflow:hidden}
  .legal-wrap{max-width:820px;margin:0 auto;padding:120px 40px 110px}
  .legal-close{position:fixed;top:30px;right:40px;font-size:12px;letter-spacing:.18em;
    text-transform:uppercase;cursor:pointer;color:var(--ink-soft);background:var(--paper);
    border:1px solid var(--line);padding:12px 20px;z-index:5}
  .legal-close:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}
  .legal-wrap .eyebrow{margin-bottom:20px}
  .legal-wrap h2{font-size:clamp(34px,5vw,54px);margin-bottom:18px;font-family:var(--serif);font-weight:300;line-height:1.08}
  .legal-wrap h2 em{font-style:italic;color:var(--bronze)}
  .legal-wrap .upd{font-size:13px;color:var(--ink-soft);letter-spacing:.04em;
    margin-bottom:50px;border-bottom:1px solid var(--line);padding-bottom:30px}
  .legal-wrap h3{font-family:var(--serif);font-size:24px;margin:44px 0 14px}
  .legal-wrap p{color:var(--ink-soft);font-size:15.5px;margin-bottom:14px}
  .legal-wrap a{color:var(--bronze-deep);border-bottom:1px solid var(--line)}
  /* SKIP TO CONTENT (accessibility / SEO) */
  .skip{position:absolute;top:-40px;left:0;background:var(--ink);color:var(--paper);
    padding:10px 16px;z-index:300;font-size:13px;letter-spacing:.1em}
  .skip:focus{top:0}
  /* RESPONSIVE */
  @media(max-width:1080px){
    .foot-top{grid-template-columns:1fr 1fr}
    .enq-grid{grid-template-columns:1fr;gap:40px}
  }
  @media(max-width:760px){
    .wrap{padding:0 24px}nav{padding:0 24px}
    .navlinks{position:fixed;inset:0;background:var(--paper);flex-direction:column;
      justify-content:center;align-items:center;gap:36px;padding:40px;
      transform:translateY(-100%);transition:.5s cubic-bezier(.16,1,.3,1);z-index:105}
    .navlinks.open{transform:translateY(0)}
    .navlinks a{font-size:20px;letter-spacing:.2em;color:var(--ink)}
    .navlinks a.cta{padding:14px 32px}
    .burger{display:flex}
    .foot-top{grid-template-columns:1fr}
    .pad{padding:90px 0}
    .page-hero{padding:140px 0 50px}
    .enquire{padding:80px 0}
    .enq-form{padding:30px 24px}
    .enq-form .form-row{grid-template-columns:1fr}
    .legal-close{top:18px;right:20px}
  }
"""


# ============================================================
# HEAD GENERATOR — produces all SEO meta + opens body
# ============================================================
def head(title, description, canonical_path, page_css="", extra_jsonld=None, og_type="website"):
    canonical = f"{SITE_URL}{canonical_path}"
    full_title = f"{title} — {BRAND}"
    og_image = f"{SITE_URL}/logo.png"

    # Base Organization JSON-LD (appears on every page)
    org_jsonld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": SITE_URL,
        "logo": og_image,
        "description": "Private watch concierge sourcing exceptional timepieces — Rolex, Patek Philippe, Audemars Piguet, Cartier and more — for collectors worldwide.",
        "telephone": PHONE,
        "email": EMAIL,
        "sameAs": [INSTAGRAM],
        "address": {"@type": "PostalAddress", "addressCountry": "GB"},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "sales",
            "email": EMAIL,
            "areaServed": "Worldwide",
            "availableLanguage": ["English"]
        }
    }
    json_lds = [json.dumps(org_jsonld, separators=(',', ':'))]
    if extra_jsonld:
        json_lds.append(json.dumps(extra_jsonld, separators=(',', ':')))
    jsonld_block = '\n'.join(
        f'<script type="application/ld+json">{j}</script>' for j in json_lds
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1A1714">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="logo.png">
<link rel="apple-touch-icon" href="logo.png">
<!-- Open Graph -->
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_GB">
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500&family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{SHARED_CSS}{page_css}</style>
{jsonld_block}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


# ============================================================
# HEADER (active highlights current page in nav)
# ============================================================
def header(active=None, solid=True):
    def cls(name):
        return ' class="on"' if active == name else ''
    cta_cls = 'class="cta on"' if active == 'enquire' else 'class="cta"'
    solid_cls = ' solid' if solid else ''
    return f"""
<header id="hdr"{(' class="solid"' if solid else '')}>
  <nav aria-label="Primary">
    <a href="index.html" aria-label="Watchmans Global — Home"><img src="logo.png" class="logo-img" alt="Watchmans Global"></a>
    <div class="navlinks">
      <a href="collection.html"{cls('collection')}>The Collection</a>
      <a href="bespoke-sourcing.html"{cls('sourcing')}>Bespoke Sourcing</a>
      <a href="process.html"{cls('process')}>Process</a>
      <a href="enquire.html" {cta_cls}>Enquire</a>
    </div>
    <button class="burger" aria-label="Open menu" aria-expanded="false" onclick="var n=document.querySelector('.navlinks'),b=this;var o=n.classList.toggle('open');b.classList.toggle('open',o);b.setAttribute('aria-expanded',o);document.body.classList.toggle('locked',o)"><span></span><span></span><span></span></button>
  </nav>
</header>
"""


# ============================================================
# ENQUIRE SECTION — appears at end of every non-enquire page
# (Lives at #enquire so it can be anchor-linked from anywhere.)
# ============================================================
def enquire_section(compact=False):
    headline_html = (
        '<h2>Tell us the watch you\'re <em>looking for</em>.</h2>'
        if not compact else
        '<h2>Begin an <em>enquiry</em>.</h2>'
    )
    return f"""
<section class="enquire" id="enquire" aria-labelledby="enquire-heading">
  <div class="wrap enq-grid">
    <div class="reveal">
      <div class="eyebrow" style="margin-bottom:26px">Begin</div>
      <div id="enquire-heading">{headline_html}</div>
      <p class="enq-lead">Send a brief and we will reply by email within one working day — usually the same day. For something more immediate, WhatsApp or call.</p>
      <div class="enq-contacts">
        <a href="{WHATSAPP}" target="_blank" rel="noopener"><b>WhatsApp</b><span>Message us directly</span></a>
        <a href="mailto:{EMAIL}"><b>Email</b><span>{EMAIL}</span></a>
        <a href="tel:{PHONE_INTL}"><b>Phone</b><span>{PHONE}</span></a>
        <a href="{INSTAGRAM}" target="_blank" rel="noopener"><b>Instagram</b><span>{INSTAGRAM_HANDLE}</span></a>
      </div>
    </div>
    <form class="enq-form reveal" id="enqForm" onsubmit="return submitEnquiry(event)" novalidate>
      <h3>Send a private enquiry</h3>
      <div class="form-sub">All correspondence is confidential.</div>
      <input type="checkbox" name="botcheck" id="" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="form-row">
        <label><span class="lbl">Name</span><input type="text" name="name" id="f_name" required autocomplete="name"></label>
        <label><span class="lbl">Email</span><input type="email" name="email" id="f_email" required autocomplete="email"></label>
      </div>
      <div class="form-row">
        <label><span class="lbl">Phone (optional)</span><input type="tel" name="phone" id="f_phone" autocomplete="tel"></label>
        <label><span class="lbl">Category</span><select name="category" id="f_cat">
          <option>Acquire from the collection</option>
          <option>Source a specific watch</option>
          <option>General enquiry</option>
        </select></label>
      </div>
      <label style="display:block;margin-bottom:8px"><span class="lbl">Your brief</span>
        <textarea name="brief" id="f_brief" placeholder="The reference, year, condition, budget — or simply what you are dreaming of." required></textarea>
      </label>
      <div class="form-foot">
        <div class="form-fine">By sending, you agree to our <a onclick="openLegal('privacy')" style="cursor:pointer;border-bottom:1px solid var(--line)">privacy notice</a>.</div>
        <button type="submit" class="btn">Send enquiry</button>
      </div>
      <div class="form-status" id="formStatus"></div>
    </form>
  </div>
</section>
"""




# ============================================================
# FOOTER + LEGAL OVERLAYS + JS (every page)
# Uses .format() so contact constants embed cleanly.
# ============================================================
def footer_and_js():
    return r"""
<footer>
  <div class="wrap">
    <div class="foot-top">
      <div>
        <img src="logo.png" class="foot-logo" alt="__BRAND__">
        <p>Your private watch concierge — sourcing exceptional timepieces for collectors who value the piece, and the silence around it.</p>
      </div>
      <div class="fcol"><h5>House</h5>
        <a href="index.html">Home</a>
        <a href="collection.html">The Collection</a>
        <a href="bespoke-sourcing.html">Bespoke Sourcing</a>
        <a href="process.html">Process</a>
      </div>
      <div class="fcol"><h5>Client</h5>
        <a href="enquire.html">Begin an Enquiry</a>
        <a href="__WHATSAPP__" target="_blank" rel="noopener">WhatsApp Us</a>
        <a href="__INSTAGRAM__" target="_blank" rel="noopener">Instagram</a>
      </div>
      <div class="fcol"><h5>Contact</h5>
        <a href="tel:__PHONE_INTL__">__PHONE__</a>
        <a href="mailto:__EMAIL__">__EMAIL__</a>
        <a href="__INSTAGRAM__" target="_blank" rel="noopener">__INSTAGRAM_HANDLE__</a>
      </div>
    </div>
    <div class="foot-bot">
      <span>&copy; <span id="yr"></span> __BRAND__. All rights reserved.</span>
      <span><a onclick="openLegal('privacy')" style="cursor:pointer">Privacy</a> &nbsp;&middot;&nbsp; <a onclick="openLegal('terms')" style="cursor:pointer">Terms</a> &nbsp;&middot;&nbsp; <a onclick="openLegal('auth')" style="cursor:pointer">Authenticity</a></span>
    </div>
  </div>
</footer>

<div class="legal-screen" id="legal" role="dialog" aria-modal="true" aria-labelledby="legalBody">
  <span class="legal-close" onclick="closeLegal()" tabindex="0" role="button">Close &times;</span>
  <div class="legal-wrap" id="legalBody"></div>
</div>

<script>
/* ===== LEGAL OVERLAYS ===== */
const LEGAL = {
  privacy: __PRIVACY_HTML__,
  terms:   __TERMS_HTML__,
  auth:    __AUTH_HTML__
};
function openLegal(k){
  document.getElementById('legalBody').innerHTML = LEGAL[k];
  document.getElementById('legal').classList.add('active');
  document.body.classList.add('locked');
  window.scrollTo(0,0);
  document.getElementById('legal').scrollTop = 0;
}
function closeLegal(){
  document.getElementById('legal').classList.remove('active');
  document.body.classList.remove('locked');
}

/* ===== ENQUIRY FORM (Web3Forms) ===== */
function submitEnquiry(e){
  e.preventDefault();
  var f = e.target;
  var data = {
    name:  f.name.value.trim(),
    email: f.email.value.trim(),
    phone: f.phone.value.trim(),
    category: f.category.value,
    brief: f.brief.value.trim()
  };
  var status = document.getElementById('formStatus');
  if (!data.name || !data.email || !data.brief) {
    status.className = 'form-status err';
    status.textContent = 'Please complete name, email and brief.';
    return false;
  }

  var btn = f.querySelector('button[type=submit]');
  var btnLabel = btn ? btn.textContent : '';
  if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
  status.className = 'form-status ok';
  status.textContent = 'Sending your enquiry…';

  var payload = {
    access_key: '__WEB3FORMS_KEY__',
    subject: 'Enquiry from ' + data.name + ' (' + data.category + ')',
    from_name: '__BRAND__ Website',
    replyto: data.email,
    botcheck: f.botcheck && f.botcheck.checked ? true : false,
    Name: data.name,
    Email: data.email,
    Phone: data.phone || '—',
    Category: data.category,
    Brief: data.brief
  };

  fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(function(r){ return r.json(); })
  .then(function(res){
    if (res.success) {
      status.className = 'form-status ok';
      status.textContent = 'Thank you, ' + data.name.split(' ')[0] +
        '. Your enquiry has reached us — we will reply by email within one working day, usually sooner.';
      f.reset();
    } else {
      status.className = 'form-status err';
      status.textContent = 'Something went wrong sending your enquiry. Please email us directly at __EMAIL__.';
    }
  })
  .catch(function(){
    status.className = 'form-status err';
    status.textContent = 'Network problem sending your enquiry. Please email us directly at __EMAIL__.';
  })
  .finally(function(){
    if (btn) { btn.disabled = false; btn.textContent = btnLabel; }
  });

  return false;
}

/* ===== HEADER SCROLL + REVEAL + YEAR + PREFILL ===== */
document.getElementById('yr').textContent = new Date().getFullYear();
var hdr = document.getElementById('hdr');
window.addEventListener('scroll', function(){
  hdr.classList.toggle('scrolled', window.scrollY > 40);
});

/* Close mobile nav when a link is tapped */
document.querySelectorAll('.navlinks a').forEach(function(a){
  a.addEventListener('click', function(){
    var n = document.querySelector('.navlinks');
    var b = document.querySelector('.burger');
    n.classList.remove('open');
    if (b) { b.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); }
    document.body.classList.remove('locked');
  });
});
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });

/* Prefill brief from ?piece=... (set by collection page) */
(function(){
  var p = new URLSearchParams(location.search).get('piece');
  if (!p) return;
  var brief = document.getElementById('f_brief');
  var cat = document.getElementById('f_cat');
  if (brief) { brief.value = "I'd like to enquire about: " + p + "\n\n"; brief.focus(); }
  if (cat) { cat.value = 'Acquire from the collection'; }
  setTimeout(function(){
    var el = document.getElementById('enquire');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }, 120);
})();
</script>
</body>
</html>
"""


# Legal-overlay HTML (returned as JS string literals).
# Kept separate for readability.
def _legal_privacy_js():
    html = (
        '<div class="eyebrow">' + BRAND + '</div>'
        '<h2>Privacy <em>Notice</em></h2>'
        '<div class="upd">How we handle the information you share with us.</div>'
        '<h3>Who we are</h3><p>' + BRAND + ' ("we", "us") is a private watch sourcing house. '
        'Reach us at <a href="mailto:' + EMAIL + '">' + EMAIL + '</a> or '
        '<a href="tel:' + PHONE_INTL + '">' + PHONE + '</a>.</p>'
        '<h3>What we collect</h3><p>Only what you choose to share through enquiries or '
        'commissions &mdash; typically name, contact details, the reference you are interested in, '
        'and any background relevant to authenticating or delivering a piece. We do not track you '
        'across the web and we do not use advertising cookies.</p>'
        '<h3>Sharing</h3><p>We never sell your data. We share only what is necessary with trusted '
        'parties to fulfil your request &mdash; for example secure logistics, escrow and '
        'authentication partners &mdash; and with our enquiry-handling provider. Your identity is '
        'never disclosed to the wider market without your instruction.</p>'
        '<h3>Third parties on this site</h3><p>This site loads typography from Google Fonts and '
        'may route enquiry messages through a form-delivery provider; these process limited '
        'technical data to function. No advertising or tracking cookies are set.</p>'
        '<h3>Retention</h3><p>We keep enquiry records only as long as needed for the relationship '
        'and any legal or accounting obligations, then delete them.</p>'
        '<h3>Your rights</h3><p>You may request access, correction or deletion of your data, or '
        'object to its use, at any time by emailing us. You may also complain to the UK '
        'Information Commissioner&rsquo;s Office (ico.org.uk).</p>'
    )
    return json.dumps(html)


def _legal_terms_js():
    html = (
        '<div class="eyebrow">' + BRAND + '</div>'
        '<h2>Terms of <em>Service</em></h2>'
        '<div class="upd">The basis on which we provide our services.</div>'
        '<h3>Our service</h3><p>' + BRAND + ' offers (i) the sale of timepieces held in our '
        'collection and (ii) bespoke sourcing, where we search for a specific reference on your '
        'behalf against an agreed brief.</p>'
        '<h3>Enquiries &amp; quotations</h3><p>Listings and indications on this site are '
        'invitations to enquire, not binding offers. Availability, specification and price are '
        'confirmed in writing before any commitment. Prices may change with the market until '
        'confirmed.</p>'
        '<h3>Sourcing commissions</h3><p>Bespoke sourcing is undertaken on terms agreed with you '
        'in advance, including scope, budget boundaries and our fee. We act in good faith but '
        'cannot guarantee that any particular reference can be located within a given timeframe.</p>'
        '<h3>Authentication, payment &amp; delivery</h3><p>Every piece is authenticated before '
        'completion. Payment terms, escrow where applicable, and fully insured delivery are set '
        'out per transaction.</p>'
        '<h3>No investment advice</h3><p>We do not provide investment, financial or tax advice. '
        'Timepieces are acquired for ownership and enjoyment; values can rise or fall and we '
        'make no representation as to future value.</p>'
        '<h3>Liability &amp; governing law</h3><p>Nothing here limits liability that cannot '
        'lawfully be limited. Otherwise our liability is limited to the value of the relevant '
        'transaction. These terms are governed by the laws of England and Wales.</p>'
    )
    return json.dumps(html)


def _legal_auth_js():
    html = (
        '<div class="eyebrow">' + BRAND + '</div>'
        '<h2>Authenticity &amp; <em>Assurance</em></h2>'
        '<div class="upd">Our commitment on every timepiece we handle.</div>'
        '<h3>Every piece, authenticated</h3><p>No watch is offered or delivered until its '
        'authenticity has been independently established. We examine movement, case, dial and '
        'components, and verify accompanying documentation where present.</p>'
        '<h3>Honest condition</h3><p>Condition is described accurately and without flattery. '
        '&ldquo;Full set&rdquo; denotes the watch with its box and papers as described; '
        '&ldquo;vintage&rdquo; pieces are assessed on their own terms with age-appropriate '
        'expectations made clear.</p>'
        '<h3>Provenance</h3><p>Where a documented history exists it is shared with you. Where it '
        'does not, we say so plainly rather than imply it.</p>'
        '<h3>Your assurance</h3><p>If an independent specialist of mutual agreement determines a '
        'delivered piece is not as represented, we will make it right &mdash; by remedy, '
        'replacement or refund &mdash; under the terms agreed for that transaction. Consumer '
        'rights for distance purchases apply where applicable under UK law.</p>'
        '<h3>Talk to us</h3><p>Any question on a specific piece &mdash; '
        '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a> or '
        '<a href="tel:' + PHONE_INTL + '">' + PHONE + '</a>.</p>'
    )
    return json.dumps(html)


def render_footer():
    """Apply all placeholder substitutions in the footer template."""
    out = footer_and_js()
    repl = {
        '__BRAND__': BRAND,
        '__WHATSAPP__': WHATSAPP,
        '__INSTAGRAM__': INSTAGRAM,
        '__INSTAGRAM_HANDLE__': INSTAGRAM_HANDLE,
        '__PHONE__': PHONE,
        '__PHONE_INTL__': PHONE_INTL,
        '__EMAIL__': EMAIL,
        '__WEB3FORMS_KEY__': WEB3FORMS_KEY,
        '__PRIVACY_HTML__': _legal_privacy_js(),
        '__TERMS_HTML__': _legal_terms_js(),
        '__AUTH_HTML__': _legal_auth_js(),
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


# ============================================================
# CATALOG DATA + IMAGE PLACEHOLDER HELPER
# ============================================================
def make_placeholder_svg(initials, variant=0):
    """Bronze-accented placeholder SVG with brand initials. Distinct per variant."""
    bg_variants = [
        ('1A1714', '3a2e1f'),
        ('2a2520', '1A1714'),
        ('3a2e1f', '1A1714'),
        ('1A1714', '2a2520'),
    ]
    bg1, bg2 = bg_variants[variant % len(bg_variants)]
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>"
        "<defs><radialGradient id='g' cx='50%' cy='48%' r='65%'>"
        f"<stop offset='0%' stop-color='%23{bg2}'/>"
        f"<stop offset='100%' stop-color='%23{bg1}'/>"
        "</radialGradient><filter id='n'>"
        "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/>"
        "<feColorMatrix type='saturate' values='0'/></filter></defs>"
        "<rect width='600' height='600' fill='url(%23g)'/>"
        "<rect width='600' height='600' filter='url(%23n)' opacity='.18'/>"
        "<circle cx='300' cy='300' r='160' fill='none' stroke='%239A7B4F' stroke-width='1.5' opacity='.55'/>"
        "<circle cx='300' cy='300' r='135' fill='none' stroke='%23F4F0E8' stroke-width='.8' opacity='.22'/>"
        f"<text x='300' y='318' text-anchor='middle' font-family='Georgia, serif' font-style='italic' "
        f"font-size='48' fill='%23F4F0E8' opacity='.82' letter-spacing='2'>{initials}</text>"
        "</svg>"
    )
    return 'data:image/svg+xml;utf8,' + svg


def collection_pieces():
    return [
        dict(id='cartier-vendome', brand='Cartier', initials='C', filter='cartier vintage',
             model='Vend\u00f4me 30mm', meta='Vintage \u00b7 Great condition',
             price='\u00a32,249', year='c. 1990', condition='Great',
             set_='Watch only \u2014 bracelet adjusted to fit',
             desc='An understated lady\'s Vend\u00f4me in yellow gold-plated steel, the case carrying the soft patina that only thirty-odd years on a wrist can give. Roman numerals, blued sword hands, sapphire crown.', n=3),
        dict(id='rolex-daytona-tiffany', brand='Rolex', initials='R', filter='rolex',
             model='Daytona "Tiffany"', meta='2026 \u00b7 New',
             price='\u00a372,000', year='2026', condition='New, unworn',
             set_='Full set, stickers intact, factory seal',
             desc='The reference 126500LN with the celebrated turquoise-blue "Tiffany" dial \u2014 a release whose desirability already exceeds list. Delivered fresh from authorised distribution with full provenance.', n=4),
        dict(id='ap-royal-oak-offshore', brand='Audemars Piguet', initials='AP', filter='ap',
             model='Royal Oak Offshore', meta='2023 \u00b7 Full set',
             price='\u00a339,000', year='2023', condition='Excellent',
             set_='Box, papers, all original links',
             desc='The 42mm Offshore in stainless steel with the "Mega Tapisserie" dial. Worn sparingly, presenting as new. A practical entry into the Offshore line without the wait.', n=3),
        dict(id='patek-5726', brand='Patek Philippe', initials='PP', filter='patek',
             model='Nautilus 5726/1A', meta='2026 \u00b7 New',
             price='\u00a3115,000', year='2026', condition='New, factory sealed',
             set_='Complete factory delivery \u2014 box, papers, seal',
             desc='The 40.5mm Nautilus Annual Calendar in stainless steel with the deep blue embossed dial and moon phase. A genuine new-old-stock placement; the kind of piece that defines a collection.', n=4),
        dict(id='rolex-skydweller-green', brand='Rolex', initials='R', filter='rolex',
             model='Sky-Dweller, Green', meta='Dec 2025 \u00b7 Full set \u00b7 New',
             price='\u00a318,500', year='2025', condition='New, unworn',
             set_='Full set, all stickers',
             desc='Reference 336934 in white-gold/steel with the green dial \u2014 the configuration Rolex chose to debut the redesigned case. December 2025 production.', n=3),
        dict(id='rolex-datejust-vintage', brand='Rolex', initials='R', filter='rolex vintage',
             model='Ladies Datejust 26mm', meta='Vintage \u00b7 Full set \u00b7 Excellent',
             price='\u00a35,495', year='c. 1987', condition='Excellent',
             set_='Full set with original papers',
             desc='A 26mm Datejust in two-tone with the original silver dial and jubilee bracelet. The case retains sharp facets and the bracelet still has reassuring weight; a beautifully kept piece.', n=3),
        dict(id='rolex-gmt-master-ii', brand='Rolex', initials='R', filter='rolex',
             model='GMT-Master II "Pepsi"', meta='2026 \u00b7 Full set \u00b7 New',
             price='\u00a313,999', year='2026', condition='New, unworn',
             set_='Full set, stickers, jubilee bracelet',
             desc='The 126710BLRO in stainless steel on the Jubilee bracelet \u2014 the most-requested configuration of the most-requested sports Rolex. Fresh delivery.', n=4),
        dict(id='rolex-datejust-36', brand='Rolex', initials='R', filter='rolex',
             model='Datejust 36', meta='2025 \u00b7 Full set \u00b7 New',
             price='\u00a38,495', year='2025', condition='New, unworn',
             set_='Full set, all stickers',
             desc='126234 in steel and white gold with the slate-grey dial and oyster bracelet. A perennial; the watch that became the wristwatch.', n=3),
        dict(id='cartier-santos-green', brand='Cartier', initials='C', filter='cartier',
             model='Santos Large, Green', meta='2024 \u00b7 Full set \u00b7 New',
             price='\u00a35,950', year='2024', condition='New, unworn',
             set_='Full set with interchangeable strap',
             desc='The large Santos in green-on-steel \u2014 a quietly excellent recent release. Includes both bracelet and leather strap with Cartier\'s quick-change system.', n=3),
        dict(id='rolex-skydweller-black', brand='Rolex', initials='R', filter='rolex',
             model='Sky-Dweller, Black', meta='2026 \u00b7 New',
             price='\u00a317,500', year='2026', condition='New, unworn',
             set_='Full set',
             desc='Reference 336934 with the black dial \u2014 the more conservative companion to its green-dial sister. Equally well-made, considerably easier to wear under a cuff.', n=3),
        dict(id='rolex-op41-pistachio', brand='Rolex', initials='R', filter='rolex',
             model='OP 41, Pistachio', meta='2025 \u00b7 Full set \u00b7 New',
             price='\u00a37,499', year='2025', condition='New, unworn',
             set_='Full set, all stickers',
             desc='Reference 124300 with the celebrated pastel pistachio dial. The everyday Oyster Perpetual elevated by an instantly recognisable colour.', n=3),
        dict(id='patek-aquanaut-5968g', brand='Patek Philippe', initials='PP', filter='patek',
             model='Aquanaut 5968G', meta='2026 \u00b7 New',
             price='\u00a399,000', year='2026', condition='New, factory sealed',
             set_='Complete factory delivery',
             desc='The Aquanaut Chronograph 5968G in white gold with the orange accents \u2014 a sporting chronograph dressed in precious metal. A piece for the collector who already has the steel.', n=4),
        dict(id='ap-50th', brand='Audemars Piguet', initials='AP', filter='ap',
             model='Royal Oak 50th Anniversary', meta='2022 \u00b7 Full set',
             price='\u00a329,850', year='2022', condition='Excellent',
             set_='Full set with anniversary documentation',
             desc='The 41mm Royal Oak from the 50th Anniversary celebration year, carrying the dedicated rotor and the deeper blue "Grande Tapisserie" dial. Lightly worn, immaculately kept.', n=3),
        dict(id='rolex-day-date-36', brand='Rolex', initials='R', filter='rolex',
             model='Day-Date 36', meta='2025 \u00b7 Full set \u00b7 New',
             price='\u00a336,000', year='2025', condition='New, unworn',
             set_='Full set, all stickers',
             desc='128238 in 18ct yellow gold with the champagne dial and president bracelet \u2014 the watch of presidents and quietly-confident industry.', n=3),
        dict(id='rolex-op41-2017', brand='Rolex', initials='R', filter='rolex vintage',
             model='Oyster Perpetual 41', meta='2017 \u00b7 Full set \u00b7 Excellent',
             price='\u00a35,950', year='2017', condition='Excellent',
             set_='Full set with original papers',
             desc='Reference 114300 in steel with the unobtrusive rhodium dial. Worn occasionally and stored properly; an honest pre-2020 OP at a reasonable level.', n=2),
    ]


# ============================================================
# HOME PAGE (index.html)
# Hero + Cinema + Marquee + Always-On Watch + Enquire
# ============================================================
def home_html():
    page_css = r"""
  /* HERO */
  .hero{min-height:92vh;display:flex;align-items:center;padding:140px 0 80px;
    position:relative;overflow:hidden;
    background:radial-gradient(900px 600px at 75% 12%,rgba(154,123,79,.14),transparent 60%),
      radial-gradient(700px 500px at 14% 90%,rgba(20,19,16,.06),transparent 55%),var(--paper)}
  .hero .wrap{position:relative;z-index:2;display:block}
  .hero-content{max-width:780px}
  .hero-eyebrow{margin-bottom:36px;display:inline-block;opacity:0;animation:rise 1s .2s forwards}
  .hero h1{font-size:clamp(54px,8vw,112px);letter-spacing:-0.025em;line-height:1.02;margin-bottom:42px}
  .hero h1 span{display:block;opacity:0;animation:rise 1s forwards}
  .hero h1 span:nth-child(1){animation-delay:.4s}
  .hero h1 span:nth-child(2){animation-delay:.6s}
  .hero h1 span:nth-child(3){animation-delay:.8s}
  .hero h1 b{font-weight:300}
  .hero h1 i{font-style:italic;color:var(--bronze)}
  .hero .lead{font-size:19px;color:var(--ink-soft);max-width:560px;line-height:1.7;
    margin-bottom:48px;opacity:0;animation:rise 1s 1s forwards}
  .hero-cta{display:flex;gap:18px;flex-wrap:wrap;opacity:0;animation:rise 1s 1.05s forwards}
  .hero-trust{margin-top:74px;display:flex;gap:54px;flex-wrap:wrap;padding-top:36px;
    border-top:1px solid var(--line);opacity:0;animation:rise 1s 1.2s forwards;max-width:880px}
  .hero-trust .t-item{display:flex;align-items:flex-start;gap:14px;flex:1;min-width:200px}
  .hero-trust .t-ic{width:30px;height:30px;display:flex;align-items:center;
    justify-content:center;color:var(--bronze);flex-shrink:0;margin-top:2px}
  .hero-trust .t-ic svg{width:24px;height:24px;stroke:var(--bronze);fill:none;
    stroke-width:1.1;opacity:.95}
  .hero-trust .t-txt{font-size:13.5px;color:var(--ink-soft);line-height:1.5}
  .hero-trust .t-txt b{display:block;color:var(--ink);font-weight:300;
    font-size:15.5px;margin-bottom:3px;font-family:var(--serif);font-style:italic}
  @keyframes rise{to{opacity:1;transform:none}}

  /* CINEMA FILM */
  .cinema{position:relative;height:100vh;min-height:600px;background:var(--dark);
    overflow:hidden;display:flex;align-items:center;justify-content:center}
  .cinema-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1}
  .cinema-overlay{position:absolute;inset:0;background:
    linear-gradient(180deg,rgba(20,19,16,.45) 0%,rgba(20,19,16,.25) 40%,rgba(20,19,16,.7) 100%);z-index:2}
  .cinema-grain{position:absolute;inset:0;opacity:.18;pointer-events:none;z-index:3;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.5'/%3E%3C/svg%3E")}
  .cinema-vignette{position:absolute;inset:0;z-index:3;pointer-events:none;
    box-shadow:inset 0 0 240px 90px rgba(0,0,0,.55)}
  .cinema-content{position:relative;z-index:4;color:var(--paper);text-align:center;
    max-width:900px;margin:0 auto;padding:0 40px}
  .cinema-eyebrow{color:var(--bronze);margin-bottom:36px;
    opacity:0;animation:rise 1.4s .3s forwards}
  .cinema h2{font-size:clamp(56px,9vw,128px);letter-spacing:-.03em;line-height:1.02;
    color:var(--paper);margin-bottom:36px;opacity:0;animation:rise 1.4s .6s forwards}
  .cinema h2 em{font-style:italic;color:var(--bronze)}
  .cinema p{font-size:19px;color:rgba(244,240,232,.78);max-width:600px;margin:0 auto 42px;
    line-height:1.7;opacity:0;animation:rise 1.4s .9s forwards}
  .cinema-cta{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;
    opacity:0;animation:rise 1.4s 1.1s forwards}
  .cinema-scroll{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);
    z-index:4;color:rgba(244,240,232,.6);font-size:11px;letter-spacing:.32em;
    text-transform:uppercase;display:flex;flex-direction:column;align-items:center;gap:12px;
    opacity:0;animation:rise 1.4s 1.4s forwards}
  .cinema-scroll i{display:block;width:1px;height:40px;background:rgba(244,240,232,.4);
    animation:dropline 2.4s ease-in-out infinite}
  @keyframes dropline{0%,100%{transform:scaleY(0);transform-origin:top}50%{transform:scaleY(1)}}

  /* ETHOS */
  .ethos{background:var(--dark);color:var(--paper)}
  .ethos .eyebrow{color:var(--bronze)}
  .ethos-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:80px;align-items:center}
  .ethos h2{font-size:clamp(34px,4.4vw,56px);color:var(--paper)}
  .ethos h2 em{font-style:italic;color:var(--bronze)}
  .ethos p{color:var(--dark-soft);font-size:18px;margin-top:30px;line-height:1.7}
  .ethos-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
    margin-top:60px;background:rgba(154,123,79,.2)}
  .ethos-stats > div{background:var(--dark);padding:52px 30px 44px;text-align:center}
  .ethos-stats .es-ic{margin:0 auto 22px;color:var(--bronze);height:54px;
    display:flex;align-items:center;justify-content:center;opacity:.92}
  .ethos-stats .es-ic svg{width:54px;height:54px}
  .ethos-stats .num{font-family:var(--serif);font-size:46px;color:var(--paper);line-height:1}
  .ethos-stats .num em{font-style:italic;color:var(--bronze);font-weight:300}
  .ethos-stats .lbl{font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;
    color:var(--dark-soft);margin-top:12px}

  @media(max-width:1080px){
    .ethos-grid{grid-template-columns:1fr;gap:46px}
  }
  @media(max-width:760px){
    .hero{min-height:auto;padding:120px 0 60px}
    .hero-trust{gap:30px;margin-top:50px}
    .hero-trust .t-item{min-width:100%}
    .ethos-stats{grid-template-columns:1fr}
    .cinema{height:80vh;min-height:480px}
  }
"""

    # JSON-LD: Organization extended with services list
    extra_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "url": SITE_URL,
        "name": BRAND,
        "publisher": {"@type": "Organization", "name": BRAND, "url": SITE_URL},
        "potentialAction": {
            "@type": "SearchAction",
            "target": SITE_URL + "/collection.html?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }

    head_html = head(
        title=TAGLINE,
        description="Watchmans Global is a private watch concierge sourcing exceptional Rolex, Patek Philippe, Audemars Piguet and Cartier timepieces for discerning collectors worldwide. Discreet. Authenticated. Considered.",
        canonical_path="/",
        page_css=page_css,
        extra_jsonld=extra_jsonld,
    )

    body = r"""
""" + header(active='home') + r"""

<main id="main">

<section class="hero" aria-labelledby="hero-h1">
  <div class="grain"></div>
  <div class="wrap">
    <div class="hero-content">
      <div class="hero-eyebrow eyebrow">""" + TAGLINE + r"""</div>
      <h1 id="hero-h1">
        <span><b>The watch</b></span>
        <span><b><i>worth waiting for,</i></b></span>
        <span><b>found for you.</b></span>
      </h1>
      <p class="lead">A personal sourcing house for the discerning collector. We watch the market so you don't have to &mdash; and quietly bring you the piece you've been looking for.</p>
      <div class="hero-cta">
        <a href="collection.html" class="btn">View the Collection</a>
        <a href="bespoke-sourcing.html" class="btn ghost">Source a Watch</a>
      </div>
      <div class="hero-trust">
        <div class="t-item">
          <div class="t-ic"><svg viewBox="0 0 24 24" fill="none"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/></svg></div>
          <div class="t-txt"><b>Independently authenticated</b>Every piece verified before it reaches you</div>
        </div>
        <div class="t-item">
          <div class="t-ic"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/></svg></div>
          <div class="t-txt"><b>Insured worldwide delivery</b>White-glove, fully covered, to your door</div>
        </div>
        <div class="t-item">
          <div class="t-ic"><svg viewBox="0 0 24 24" fill="none"><rect x="5" y="11" width="14" height="10" rx="1.5"/><path d="M8 11V7a4 4 0 018 0v4"/></svg></div>
          <div class="t-txt"><b>Absolute discretion</b>Your name never enters the market</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="cinema" id="cinema" aria-label="Watchmans Film">
  <video class="cinema-video" autoplay muted loop playsinline
         poster="data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'%3E%3Cdefs%3E%3CradialGradient id='g' cx='50%25' cy='42%25' r='75%25'%3E%3Cstop offset='0%25' stop-color='%23242018'/%3E%3Cstop offset='55%25' stop-color='%23151210'/%3E%3Cstop offset='100%25' stop-color='%23080706'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect width='1600' height='900' fill='url(%23g)'/%3E%3C/svg%3E">
    <!-- Replace with your luxury-watch film (1080p MP4, ~10-30s, muted-friendly): -->
    <source src="" type="video/mp4">
  </video>
  <div class="cinema-overlay"></div>
  <div class="cinema-grain"></div>
  <div class="cinema-vignette"></div>
  <div class="wrap cinema-content">
    <div class="cinema-eyebrow eyebrow">Watchmans &middot; The Film</div>
    <h2>Quietly <em>extraordinary.</em></h2>
    <p>A private window onto the watches we live with &mdash; references rarely seen, conversations rarely had, and the considered moments before a piece changes hands.</p>
    <div class="cinema-cta">
      <a href="collection.html" class="btn light">View the Collection</a>
      <a href="bespoke-sourcing.html" class="btn light">Begin a Private Search</a>
    </div>
  </div>
  <div class="cinema-scroll" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <span>Rolex</span><span>Patek Philippe</span><span>Audemars Piguet</span><span>Cartier</span><span>A. Lange &amp; S&ouml;hne</span><span>F.P. Journe</span>
    <span>Rolex</span><span>Patek Philippe</span><span>Audemars Piguet</span><span>Cartier</span><span>A. Lange &amp; S&ouml;hne</span><span>F.P. Journe</span>
  </div>
</div>

<section class="ethos pad" aria-labelledby="ethos-h2">
  <div class="wrap ethos-grid">
    <div class="reveal">
      <div class="eyebrow" style="margin-bottom:28px">Always On Watch</div>
      <h2 id="ethos-h2">A personal shopper, <em>for watches</em>.</h2>
      <p>Watchmans is not a marketplace. We are the person you call when you want a specific timepiece found, vetted and delivered &mdash; without spending your evenings refreshing listings or wondering who to trust. Provenance first. Discretion always.</p>
    </div>
    <div class="ethos-stats reveal">
      <div>
        <div class="es-ic"><svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="1.1"><circle cx="28" cy="28" r="20"/><path d="M28 14v14l9 6"/><path d="M28 6v3M28 47v3M6 28h3M47 28h3"/></svg></div>
        <div class="num">4<em>+</em></div><div class="lbl">Years Sourcing</div>
      </div>
      <div>
        <div class="es-ic"><svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="1.1"><circle cx="12" cy="14" r="3.2"/><circle cx="44" cy="14" r="3.2"/><circle cx="28" cy="28" r="3.6"/><circle cx="12" cy="42" r="3.2"/><circle cx="44" cy="42" r="3.2"/><path d="M14.5 16L25 26M41.5 16L31 26M14.5 40L25 30M41.5 40L31 30M15 14h26M15 42h26"/></svg></div>
        <div class="num">100<em>+</em></div><div class="lbl">Vetted Partners</div>
      </div>
      <div>
        <div class="es-ic"><svg viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="1.1"><circle cx="28" cy="28" r="20"/><ellipse cx="28" cy="28" rx="20" ry="8"/><ellipse cx="28" cy="28" rx="8" ry="20"/><path d="M8 28h40"/><path d="M28 8a26 26 0 010 40M28 8a26 26 0 000 40"/></svg></div>
        <div class="num">5</div><div class="lbl">Continents Networked</div>
      </div>
    </div>
  </div>
</section>

""" + enquire_section() + r"""

</main>
""" + render_footer()

    return head_html + body


# ============================================================
# COLLECTION PAGE (collection.html)
# Page hero + filter bar + grid + multi-image gallery modal
# ============================================================
def collection_html():
    pieces = collection_pieces()

    # Build ItemList JSON-LD with all pieces as Products (good for SEO)
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Watchmans Global — Available Collection",
        "numberOfItems": len(pieces),
        "itemListElement": []
    }
    for i, p in enumerate(pieces, 1):
        item_list["itemListElement"].append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Product",
                "name": f"{p['brand']} {p['model']}",
                "description": p['desc'],
                "brand": {"@type": "Brand", "name": p['brand']},
                "offers": {
                    "@type": "Offer",
                    "priceCurrency": "GBP",
                    "price": p['price'].replace('£', '').replace(',', ''),
                    "availability": "https://schema.org/InStock",
                    "url": f"{SITE_URL}/collection.html#{p['id']}"
                }
            }
        })

    page_css = r"""
  .col-tools{margin-top:40px;display:flex;justify-content:space-between;
    align-items:flex-end;flex-wrap:wrap;gap:30px}
  .filters{display:flex;gap:8px;flex-wrap:wrap}
  .filters button{font-family:var(--sans);font-size:12px;letter-spacing:.16em;
    text-transform:uppercase;font-weight:500;padding:11px 22px;border:1px solid var(--line);
    background:transparent;color:var(--ink-soft);cursor:pointer;transition:.3s}
  .filters button:hover{border-color:var(--ink);color:var(--ink)}
  .filters button.on{background:var(--ink);color:var(--paper);border-color:var(--ink)}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:50px}
  .piece{background:var(--paper);border:1px solid var(--line);cursor:pointer;
    transition:.5s;position:relative;display:flex;flex-direction:column}
  .piece:hover{border-color:var(--bronze);transform:translateY(-4px);
    box-shadow:0 22px 50px -28px rgba(20,19,16,.28)}
  .piece .ph{aspect-ratio:1/1;position:relative;overflow:hidden;background:var(--dark)}
  .piece .ph img{width:100%;height:100%;object-fit:cover;transition:.7s}
  .piece:hover .ph img{transform:scale(1.04)}
  .piece .badge{position:absolute;top:14px;left:14px;background:var(--paper);
    color:var(--ink);font-size:10px;letter-spacing:.22em;text-transform:uppercase;
    padding:7px 12px;font-weight:600;z-index:2}
  .piece .imgcount{position:absolute;bottom:14px;right:14px;background:rgba(20,19,16,.7);
    color:var(--paper);font-size:11px;letter-spacing:.08em;padding:5px 10px;z-index:2;
    display:flex;align-items:center;gap:6px;backdrop-filter:blur(8px)}
  .piece .imgcount svg{width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5}
  .piece .body{padding:26px 26px 28px;flex:1;display:flex;flex-direction:column}
  .piece .brand{font-size:10.5px;letter-spacing:.26em;color:var(--bronze-deep);
    text-transform:uppercase;font-weight:600;margin-bottom:10px}
  .piece h3{font-size:22px;margin-bottom:6px;line-height:1.15}
  .piece .meta{font-size:13.5px;color:var(--ink-soft);margin-bottom:18px;letter-spacing:.02em}
  .piece .foot{display:flex;justify-content:space-between;align-items:baseline;
    border-top:1px solid var(--line);padding-top:18px;margin-top:auto}
  .piece .price{font-family:var(--serif);font-size:21px;color:var(--ink);font-weight:400}
  .piece .enq{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--bronze-deep)}
  .col-foot{margin-top:60px;text-align:center;font-size:14.5px;color:var(--ink-soft)}
  .col-foot a{color:var(--bronze-deep);border-bottom:1px solid var(--line);cursor:pointer;padding-bottom:2px}
  /* Multi-image gallery modal */
  .modal{display:none;position:fixed;inset:0;z-index:300;background:rgba(20,19,16,.85);
    backdrop-filter:blur(8px);align-items:center;justify-content:center;padding:40px 20px;overflow-y:auto}
  .modal.active{display:flex}
  .m-card{background:var(--paper);max-width:1080px;width:100%;display:grid;
    grid-template-columns:1.15fr .85fr;position:relative;max-height:90vh;overflow:hidden}
  .m-close{position:absolute;top:20px;right:20px;width:38px;height:38px;
    border-radius:50%;background:var(--paper);border:1px solid var(--line);cursor:pointer;
    z-index:5;display:flex;align-items:center;justify-content:center;font-size:18px}
  .m-close:hover{background:var(--ink);color:var(--paper)}
  .gallery-wrap{background:var(--dark);position:relative;display:flex;flex-direction:column}
  .gallery-main{flex:1;position:relative;min-height:380px;display:flex;align-items:center;justify-content:center}
  .gallery-main img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
  .gallery-arrow{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;
    background:rgba(244,240,232,.85);border:0;cursor:pointer;z-index:3;display:flex;
    align-items:center;justify-content:center;backdrop-filter:blur(6px);transition:.3s;font-size:20px}
  .gallery-arrow:hover{background:var(--paper)}
  .gallery-arrow.prev{left:14px}.gallery-arrow.next{right:14px}
  .gallery-count{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);
    background:rgba(20,19,16,.75);color:var(--paper);font-size:11px;letter-spacing:.16em;
    padding:6px 14px;z-index:3;backdrop-filter:blur(6px)}
  .gallery-thumbs{display:flex;gap:6px;padding:10px;background:rgba(20,19,16,.9);overflow-x:auto}
  .gallery-thumbs button{width:64px;height:64px;border:1px solid transparent;background:none;
    cursor:pointer;padding:0;flex-shrink:0;opacity:.55;transition:.3s}
  .gallery-thumbs button.on,.gallery-thumbs button:hover{opacity:1;border-color:var(--bronze)}
  .gallery-thumbs img{width:100%;height:100%;object-fit:cover}
  .m-meta{padding:40px 38px;overflow-y:auto}
  .m-meta .eyebrow{margin-bottom:18px}
  .m-meta h2{font-size:30px;margin-bottom:8px}
  .m-meta .m-sub{font-size:14px;color:var(--ink-soft);margin-bottom:24px}
  .m-meta .m-price{font-family:var(--serif);font-size:30px;color:var(--ink);
    margin-bottom:26px;padding-bottom:24px;border-bottom:1px solid var(--line)}
  .m-spec{display:grid;grid-template-columns:1fr;gap:16px;margin-bottom:26px}
  .m-spec .s-r{display:grid;grid-template-columns:.4fr 1fr;gap:14px;font-size:14px;
    padding-bottom:14px;border-bottom:1px solid var(--line)}
  .m-spec .s-l{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--bronze-deep);font-weight:600;padding-top:2px}
  .m-spec .s-v{color:var(--ink)}
  .m-desc{font-size:14.5px;color:var(--ink-soft);line-height:1.7;margin-bottom:26px}
  .m-cta{display:flex;flex-direction:column;gap:10px}
  .m-cta .btn{width:100%;text-align:center}
  .m-fine{font-size:12px;color:var(--ink-soft);text-align:center;margin-top:14px;line-height:1.5}
  @media(max-width:880px){
    .grid{grid-template-columns:repeat(2,1fr)}
    .m-card{grid-template-columns:1fr;max-height:95vh;overflow-y:auto}
    .gallery-main{min-height:300px}
  }
  @media(max-width:560px){
    .grid{grid-template-columns:1fr}
  }
"""

    head_html = head(
        title="The Collection — Vetted Timepieces Available Now",
        description="Browse the Watchmans Global collection of authenticated Rolex, Patek Philippe, Audemars Piguet and Cartier timepieces — each held in hand, verified, and ready for discreet acquisition.",
        canonical_path="/collection.html",
        page_css=page_css,
        extra_jsonld=item_list,
    )

    # Build piece-cards markup (server-side rendered for SEO crawlability)
    cards_html = ""
    for p in pieces:
        ph_img = make_placeholder_svg(p['initials'], variant=hash(p['id']) % 4)
        badge = ('New' if 'New' in p['condition'] else 'Vintage' if 'Vintage' in p['filter'] or 'Vintage' in p['meta'] else 'Available')
        cards_html += (
            f'<article class="piece" data-f="{p["filter"]}" data-id="{p["id"]}" '
            f'onclick="openModal(\'{p["id"]}\')" id="{p["id"]}">'
            f'<div class="ph">'
            f'<img src="{ph_img}" alt="{p["brand"]} {p["model"]}" loading="lazy">'
            f'<span class="badge">{badge}</span>'
            f'<span class="imgcount"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="1"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/></svg>{p["n"]}</span>'
            f'</div>'
            f'<div class="body">'
            f'<div class="brand">{p["brand"]}</div>'
            f'<h3>{p["model"]}</h3>'
            f'<div class="meta">{p["meta"]}</div>'
            f'<div class="foot"><span class="price">{p["price"]}</span><span class="enq">Enquire &rarr;</span></div>'
            f'</div></article>\n'
        )

    # JS catalog (for modal rendering)
    js_catalog = []
    for p in pieces:
        imgs = [make_placeholder_svg(p['initials'], variant=(hash(p['id']) + i) % 4) for i in range(p['n'])]
        js_catalog.append({
            'id': p['id'],
            'brand': p['brand'],
            'model': p['model'],
            'meta': p['meta'],
            'price': p['price'],
            'year': p['year'],
            'condition': p['condition'],
            'set': p['set_'],
            'desc': p['desc'],
            'images': imgs,
        })

    body = r"""
""" + header(active='collection') + r"""

<main id="main">

<section class="page-hero" aria-labelledby="col-h1">
  <div class="grain"></div>
  <div class="wrap">
    <div class="eyebrow reveal">Available Now</div>
    <h1 id="col-h1" class="reveal">The <em>Collection</em></h1>
    <p class="lead reveal">A curated selection of authenticated timepieces, held in hand and ready for discreet acquisition. Each piece verified before it is offered. Tap any reference to view full detail and enquire.</p>
  </div>
</section>

<section class="pad" style="padding-top:50px">
  <div class="wrap">
    <div class="col-tools reveal">
      <div class="filters" id="filters" role="tablist" aria-label="Filter by brand">
        <button class="on" data-f="all">All</button>
        <button data-f="rolex">Rolex</button>
        <button data-f="patek">Patek Philippe</button>
        <button data-f="ap">Audemars Piguet</button>
        <button data-f="cartier">Cartier</button>
        <button data-f="vintage">Vintage</button>
      </div>
    </div>
    <div class="grid reveal" id="grid">
""" + cards_html + r"""
    </div>
    <div class="col-foot reveal">
      Not seeing the reference you want? <a href="bespoke-sourcing.html">Commission a private search &rarr;</a>
    </div>
  </div>
</section>

""" + enquire_section() + r"""

</main>

<!-- Gallery modal -->
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="m-h2" onclick="if(event.target===this)closeModal()">
  <article class="m-card" id="mCard">
    <button class="m-close" onclick="closeModal()" aria-label="Close">&times;</button>
    <div class="gallery-wrap">
      <div class="gallery-main" id="galMain"></div>
      <button class="gallery-arrow prev" id="galPrev" onclick="galleryStep(-1)" aria-label="Previous">&larr;</button>
      <button class="gallery-arrow next" id="galNext" onclick="galleryStep(1)" aria-label="Next">&rarr;</button>
      <span class="gallery-count" id="galCount"></span>
      <div class="gallery-thumbs" id="galThumbs"></div>
    </div>
    <div class="m-meta">
      <div class="eyebrow" id="m-brand"></div>
      <h2 id="m-h2"></h2>
      <div class="m-sub" id="m-sub"></div>
      <div class="m-price" id="m-price"></div>
      <div class="m-spec" id="m-spec"></div>
      <div class="m-desc" id="m-desc"></div>
      <div class="m-cta">
        <a class="btn" id="m-enq">Enquire about this piece</a>
        <a class="btn ghost" href="enquire.html">Talk to a specialist</a>
      </div>
      <div class="m-fine">Each piece is independently authenticated. Insured delivery worldwide.</div>
    </div>
  </article>
</div>

<script>
const CATALOG = """ + json.dumps(js_catalog, separators=(',', ':')) + r""";
const BY_ID = Object.fromEntries(CATALOG.map(p => [p.id, p]));

// Filter
document.querySelectorAll('#filters button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#filters button').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
    const f = btn.dataset.f;
    document.querySelectorAll('.piece').forEach(card => {
      card.style.display = (f === 'all' || card.dataset.f.includes(f)) ? '' : 'none';
    });
  });
});

// Gallery state
let galIdx = 0, galPiece = null;

function openModal(id){
  galPiece = BY_ID[id];
  if (!galPiece) return;
  galIdx = 0;
  document.getElementById('m-brand').textContent = galPiece.brand;
  document.getElementById('m-h2').textContent = galPiece.model;
  document.getElementById('m-sub').textContent = galPiece.meta;
  document.getElementById('m-price').textContent = galPiece.price;
  const spec = [
    ['Year', galPiece.year],
    ['Condition', galPiece.condition],
    ['Set', galPiece.set],
  ];
  document.getElementById('m-spec').innerHTML = spec.map(
    r => '<div class="s-r"><div class="s-l">' + r[0] + '</div><div class="s-v">' + r[1] + '</div></div>'
  ).join('');
  document.getElementById('m-desc').textContent = galPiece.desc;
  document.getElementById('m-enq').href = 'enquire.html?piece=' + encodeURIComponent(galPiece.brand + ' ' + galPiece.model);
  renderGallery();
  document.getElementById('modal').classList.add('active');
  document.body.classList.add('locked');
}
function closeModal(){
  document.getElementById('modal').classList.remove('active');
  document.body.classList.remove('locked');
}
function renderGallery(){
  if (!galPiece) return;
  const main = document.getElementById('galMain');
  main.innerHTML = '<img src="' + galPiece.images[galIdx] + '" alt="' + galPiece.brand + ' ' + galPiece.model + '">';
  document.getElementById('galCount').textContent = (galIdx + 1) + ' / ' + galPiece.images.length;
  document.getElementById('galThumbs').innerHTML = galPiece.images.map(
    (src, i) => '<button class="' + (i === galIdx ? 'on' : '') + '" onclick="setImage(' + i + ')"><img src="' + src + '" alt=""></button>'
  ).join('');
  const show = galPiece.images.length > 1;
  document.getElementById('galPrev').style.display = show ? '' : 'none';
  document.getElementById('galNext').style.display = show ? '' : 'none';
}
function setImage(i){ galIdx = i; renderGallery(); }
function galleryStep(n){
  if (!galPiece) return;
  galIdx = (galIdx + n + galPiece.images.length) % galPiece.images.length;
  renderGallery();
}
document.addEventListener('keydown', e => {
  if (!document.getElementById('modal').classList.contains('active')) return;
  if (e.key === 'Escape') closeModal();
  else if (e.key === 'ArrowLeft') galleryStep(-1);
  else if (e.key === 'ArrowRight') galleryStep(1);
});
</script>

""" + render_footer()

    return head_html + body


# ============================================================
# BESPOKE SOURCING PAGE (bespoke-sourcing.html)
# Clientele + authentication + discretion (no process — that's its own page)
# ============================================================
def sourcing_html():
    page_css = r"""
  .bs-intro{padding:100px 0 80px}
  .bs-intro .wrap{display:grid;grid-template-columns:1fr 1.1fr;gap:80px;align-items:start}
  .bs-intro .eyebrow{margin-bottom:24px}
  .bs-intro h2{font-size:clamp(34px,4.2vw,52px);margin-bottom:28px;line-height:1.1}
  .bs-intro h2 em{font-style:italic;color:var(--bronze)}
  .bs-intro p{font-size:17.5px;color:var(--ink-soft);line-height:1.75;margin-bottom:20px}
  .bs-pull{padding:60px 50px;border-left:2px solid var(--bronze);background:var(--paper-2);
    font-family:var(--serif);font-style:italic;font-size:23px;color:var(--ink);
    line-height:1.4;position:relative}
  .bs-pull .by{display:block;margin-top:24px;font-family:var(--sans);font-style:normal;
    font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--bronze-deep);font-weight:600}

  .clientele{background:var(--dark);color:var(--paper);padding:110px 0}
  .clientele .eyebrow{color:var(--bronze)}
  .clientele h2{font-size:clamp(36px,4.4vw,56px);color:var(--paper);margin:24px 0 26px}
  .clientele h2 em{font-style:italic;color:var(--bronze)}
  .clientele .lead{font-size:17px;color:var(--dark-soft);max-width:680px;line-height:1.7;margin-bottom:60px}
  .cli-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(154,123,79,.18)}
  .cli-card{background:var(--dark);padding:48px 38px;border-top:1px solid rgba(154,123,79,.25)}
  .cli-card .rom{font-family:var(--serif);font-style:italic;font-size:30px;color:var(--bronze);
    margin-bottom:16px;font-weight:300}
  .cli-card h3{font-size:22px;color:var(--paper);margin-bottom:14px;font-weight:300}
  .cli-card p{font-size:14.5px;color:var(--dark-soft);line-height:1.7}

  .auth-sec{background:var(--paper-2);padding:110px 0}
  .auth-sec .wrap{display:grid;grid-template-columns:.95fr 1.15fr;gap:80px;align-items:start}
  .auth-sec .eyebrow{margin-bottom:24px}
  .auth-sec h2{font-size:clamp(34px,4.2vw,52px);margin-bottom:24px;line-height:1.1}
  .auth-sec h2 em{font-style:italic;color:var(--bronze)}
  .auth-sec .blockquote{font-family:var(--serif);font-style:italic;font-size:20px;
    color:var(--ink);line-height:1.5;border-left:2px solid var(--bronze);
    padding:8px 0 8px 30px;margin-bottom:32px}
  .auth-sec p{font-size:16px;color:var(--ink-soft);line-height:1.75;margin-bottom:18px}
  .auth-list{display:flex;flex-direction:column;gap:22px}
  .auth-list .ar{display:grid;grid-template-columns:50px 1fr;gap:18px;
    padding-bottom:22px;border-bottom:1px solid var(--line)}
  .auth-list .ar:last-child{border:0}
  .auth-list .ar .n{font-family:var(--serif);font-style:italic;font-size:24px;color:var(--bronze)}
  .auth-list .ar h4{font-size:18px;margin-bottom:6px;font-weight:300}
  .auth-list .ar p{font-size:14.5px;color:var(--ink-soft);line-height:1.65;margin:0}

  .discretion{background:var(--dark);color:var(--paper);padding:110px 0;position:relative;overflow:hidden}
  .discretion::before{content:"";position:absolute;inset:0;
    background:radial-gradient(900px 600px at 80% 20%,rgba(154,123,79,.16),transparent 60%),
      radial-gradient(700px 500px at 10% 90%,rgba(154,123,79,.08),transparent 55%);pointer-events:none}
  .discretion .wrap{position:relative;z-index:2}
  .discretion .eyebrow{color:var(--bronze)}
  .discretion h2{font-size:clamp(34px,4.2vw,52px);color:var(--paper);margin:24px 0 22px;line-height:1.1}
  .discretion h2 em{font-style:italic;color:var(--bronze)}
  .discretion .lead{font-size:17.5px;color:var(--dark-soft);max-width:700px;line-height:1.7;margin-bottom:60px}
  .d-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:40px;margin-top:50px}
  .d-point{padding:32px 30px;border:1px solid rgba(154,123,79,.3);background:rgba(20,19,16,.5)}
  .d-point h4{font-size:19px;color:var(--paper);margin-bottom:12px;font-weight:300}
  .d-point h4 em{font-style:italic;color:var(--bronze)}
  .d-point p{font-size:14.5px;color:var(--dark-soft);line-height:1.7}

  .bs-cta{padding:110px 0;text-align:center;background:var(--paper)}
  .bs-cta h2{font-size:clamp(36px,4.6vw,60px);margin-bottom:24px;line-height:1.1}
  .bs-cta h2 em{font-style:italic;color:var(--bronze)}
  .bs-cta p{font-size:18px;color:var(--ink-soft);max-width:600px;margin:0 auto 38px;line-height:1.7}

  @media(max-width:1080px){
    .bs-intro .wrap,.auth-sec .wrap{grid-template-columns:1fr;gap:50px}
    .cli-grid{grid-template-columns:1fr 1fr}
    .d-grid{grid-template-columns:1fr}
  }
  @media(max-width:760px){
    .cli-grid{grid-template-columns:1fr}
  }
"""

    extra_jsonld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Bespoke Watch Sourcing",
        "provider": {"@type": "Organization", "name": BRAND, "url": SITE_URL},
        "serviceType": "Private watch sourcing and acquisition",
        "areaServed": "Worldwide",
        "description": "Discreet, authenticated sourcing of specific watch references for private collectors, family offices and executives. Every piece independently verified before delivery.",
        "audience": {
            "@type": "Audience",
            "audienceType": "Private collectors, family offices, executives, international clients"
        }
    }

    head_html = head(
        title="Bespoke Sourcing — Private Watch Commission",
        description="Watchmans Global offers discreet bespoke sourcing for collectors, family offices and executives. Specific references located, independently authenticated, and delivered confidentially worldwide.",
        canonical_path="/bespoke-sourcing.html",
        page_css=page_css,
        extra_jsonld=extra_jsonld,
    )

    body = r"""
""" + header(active='sourcing') + r"""

<main id="main">

<section class="page-hero" aria-labelledby="bs-h1">
  <div class="grain"></div>
  <div class="wrap">
    <div class="eyebrow reveal">Private Commission</div>
    <h1 id="bs-h1" class="reveal">Bespoke <em>Sourcing</em>.</h1>
    <p class="lead reveal">For the references you do not see listed &mdash; the piece, the year, the dial. We watch the market on your behalf and quietly bring you the watch you have been looking for.</p>
  </div>
</section>

<section class="bs-intro">
  <div class="wrap">
    <div class="reveal">
      <div class="eyebrow">Our Practice</div>
      <h2>For watches that are <em>not in any window</em>.</h2>
      <p>The watches most worth owning rarely advertise themselves. They move between collectors quietly, often without ever appearing on a public listing. Our practice is built around those conversations.</p>
      <p>You tell us the reference, the year, the dial; we work patiently and discreetly across our network until the right example surfaces. Authenticated before it reaches you. Insured to your door.</p>
    </div>
    <div class="bs-pull reveal">
      "The right watch finds you when the right people are looking."
      <span class="by">&mdash; Watchmans Global</span>
    </div>
  </div>
</section>

<section class="clientele" aria-labelledby="cli-h2">
  <div class="wrap">
    <div class="eyebrow reveal">Who We Work With</div>
    <h2 id="cli-h2" class="reveal">A relationship, <em>not a transaction</em>.</h2>
    <p class="lead reveal">Our clients come to us through introduction and stay through trust. Many are looking for one specific reference; others are quietly building over years. All are treated with the same discretion.</p>
    <div class="cli-grid">
      <article class="cli-card reveal"><div class="rom">i.</div><h3>Private Collectors</h3><p>Established collectors looking for the next considered acquisition &mdash; usually a specific reference, often without papers but with a clear story.</p></article>
      <article class="cli-card reveal"><div class="rom">ii.</div><h3>Family Offices</h3><p>Trusted to manage acquisitions on behalf of principals who value time and silence above price. Documentation handled to the standard you require.</p></article>
      <article class="cli-card reveal"><div class="rom">iii.</div><h3>Founders &amp; Executives</h3><p>The watch as the considered counterpart to a working life &mdash; chosen carefully, worn daily, kept for decades.</p></article>
      <article class="cli-card reveal"><div class="rom">iv.</div><h3>Collectors&rsquo; Spouses</h3><p>Quiet commissions on behalf of someone who already has every reference they will openly admit to wanting. Surprises managed with care.</p></article>
      <article class="cli-card reveal"><div class="rom">v.</div><h3>International Clients</h3><p>Acquisitions arranged across borders &mdash; with appropriate documentation, customs handling and fully insured logistics to anywhere in the world.</p></article>
      <article class="cli-card reveal"><div class="rom">vi.</div><h3>By Introduction</h3><p>The majority of our work arrives by quiet referral. If a current client has suggested you reach us, please mention them when you write.</p></article>
    </div>
  </div>
</section>

<section class="auth-sec" aria-labelledby="auth-h2">
  <div class="wrap">
    <div class="reveal">
      <div class="eyebrow">Authentication &amp; Provenance</div>
      <h2 id="auth-h2">Every piece, <em>verified</em>.</h2>
      <div class="blockquote">No watch leaves our hands until its authenticity has been independently established.</div>
      <p>Across pre-owned, vintage and grey-market acquisitions, authentication is the work that earns trust. We examine each piece in person and engage independent specialists where the reference or value warrants it.</p>
      <p>Where a documented history exists it is shared with you. Where it does not, we say so plainly rather than imply it.</p>
    </div>
    <div class="reveal">
      <div class="auth-list">
        <div class="ar"><div class="n">i.</div><div><h4>Movement Inspection</h4><p>Calibre, serial, finishing and operation independently verified against factory references for the period.</p></div></div>
        <div class="ar"><div class="n">ii.</div><div><h4>Case &amp; Dial Examination</h4><p>Original components confirmed; refinishing, service dials and luminous compound assessed with the appropriate magnification.</p></div></div>
        <div class="ar"><div class="n">iii.</div><div><h4>Documentation Verification</h4><p>Warranty cards, service records, and receipts cross-checked against manufacturer and dealer records where available.</p></div></div>
        <div class="ar"><div class="n">iv.</div><div><h4>Service History</h4><p>Records traced where possible; previous service work assessed for impact on originality.</p></div></div>
        <div class="ar"><div class="n">v.</div><div><h4>Market Comparison</h4><p>Final pricing benchmarked against recent comparable sales so you know exactly where the piece sits in the market.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="discretion" aria-labelledby="dis-h2">
  <div class="wrap">
    <div class="reveal">
      <div class="eyebrow">Discretion &amp; Confidentiality</div>
      <h2 id="dis-h2">The work that <em>does not happen on a screen</em>.</h2>
      <p class="lead">Our network is built on years of relationships that exist precisely because they are not advertised. The pieces that move through us do so quietly &mdash; and your involvement does the same.</p>
    </div>
    <div class="d-grid reveal">
      <div class="d-point"><h4>Your <em>name never enters the market</em></h4><p>Enquiries are made on our behalf, not yours. Sellers know there is a buyer for the piece; they do not know who.</p></div>
      <div class="d-point"><h4>No <em>public listings</em></h4><p>Pieces we hold in confidence are never published. The collection page reflects what is openly for sale; everything else stays in private channels.</p></div>
      <div class="d-point"><h4>Documentation <em>to your standard</em></h4><p>Invoices, customs paperwork and provenance records prepared in whichever name and form is most useful to you.</p></div>
      <div class="d-point"><h4>The <em>conversation stays here</em></h4><p>What is discussed in our enquiries remains between us. We never share client details or interests, in either direction.</p></div>
    </div>
  </div>
</section>

<section class="bs-cta">
  <div class="wrap reveal">
    <h2>Tell us the watch you&apos;re <em>looking for</em>.</h2>
    <p>A brief paragraph is enough to begin. We will reply by email within one working day &mdash; usually the same day.</p>
    <a href="enquire.html" class="btn">Begin a Private Search</a>
  </div>
</section>

""" + enquire_section() + r"""

</main>
""" + render_footer()

    return head_html + body


# ============================================================
# PROCESS PAGE (process.html)
# 6-step process + Assurances
# ============================================================
def process_html():
    page_css = r"""
  .proc-list{padding:90px 0 60px}
  .proc-step{display:grid;grid-template-columns:140px 1fr 1.1fr;gap:50px;
    padding:54px 0;border-bottom:1px solid var(--line);position:relative;align-items:start}
  .proc-step:last-child{border-bottom:0}
  .proc-step:hover .proc-num{color:var(--bronze)}
  .proc-num{font-family:var(--serif);font-style:italic;font-size:56px;color:var(--ink-soft);
    transition:.4s;line-height:1;font-weight:300}
  .proc-step h3{font-size:30px;font-weight:300;line-height:1.2;letter-spacing:-.01em}
  .proc-step h3 em{font-style:italic;color:var(--bronze)}
  .proc-step .pd{font-size:16px;color:var(--ink-soft);line-height:1.75}
  .proc-step .pd p{margin-bottom:14px}
  .proc-step .pd p:last-child{margin-bottom:0}

  .assure-sec{background:var(--paper-2);padding:110px 0}
  .assure-sec .sec-head{display:grid;grid-template-columns:1fr 1.1fr;gap:80px;
    align-items:end;margin-bottom:70px}
  .assure-sec .sec-head h2{font-size:clamp(36px,4.4vw,56px);line-height:1.1}
  .assure-sec .sec-head h2 em{font-style:italic;color:var(--bronze)}
  .assure-sec .sec-head .sh-r{font-size:16px;color:var(--ink-soft);line-height:1.7;padding-bottom:10px}
  .assure{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
    background:var(--line);border:1px solid var(--line)}
  .assure > div{background:var(--paper);padding:48px 32px}
  .assure .ic{font-family:var(--serif);font-style:italic;font-size:30px;color:var(--bronze);
    margin-bottom:18px;font-weight:300}
  .assure h4{font-size:21px;margin-bottom:12px;font-weight:300}
  .assure p{font-size:14.5px;color:var(--ink-soft);line-height:1.65}

  .proc-cta{padding:110px 0;text-align:center}
  .proc-cta h2{font-size:clamp(34px,4.2vw,52px);margin-bottom:20px;line-height:1.1}
  .proc-cta h2 em{font-style:italic;color:var(--bronze)}
  .proc-cta p{font-size:17px;color:var(--ink-soft);max-width:560px;margin:0 auto 36px;line-height:1.7}

  @media(max-width:880px){
    .proc-step{grid-template-columns:1fr;gap:18px}
    .proc-num{font-size:42px}
    .assure-sec .sec-head{grid-template-columns:1fr;gap:30px}
    .assure{grid-template-columns:1fr 1fr}
  }
  @media(max-width:560px){
    .assure{grid-template-columns:1fr}
  }
"""

    extra_jsonld = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "Acquiring a watch through Watchmans Global",
        "description": "Our six-stage process for sourcing, authenticating and delivering an exceptional timepiece — from first conversation to final handover.",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "The Private Briefing", "text": "A confidential conversation to establish what you are looking for — reference, year, dial, condition, budget."},
            {"@type": "HowToStep", "position": 2, "name": "The Mandate & The Search", "text": "We agree the scope and engage our private network of dealers, collectors and auction-house contacts."},
            {"@type": "HowToStep", "position": 3, "name": "Vetting & Negotiation", "text": "Each candidate is shortlisted, photographed, and quietly negotiated on your behalf — without disclosing you."},
            {"@type": "HowToStep", "position": 4, "name": "Independent Verification", "text": "Authentication is established before completion; movement, case, dial and documentation independently verified."},
            {"@type": "HowToStep", "position": 5, "name": "Escrow & Settlement", "text": "Payment routed through escrow where appropriate; documentation prepared to your specification."},
            {"@type": "HowToStep", "position": 6, "name": "Delivery & Handover", "text": "Fully insured, white-glove delivery worldwide — to your door, your office, or any address you prefer."}
        ]
    }

    head_html = head(
        title="The Process — From Brief to Wrist",
        description="The six-stage Watchmans Global process for acquiring an exceptional timepiece. From private briefing to insured worldwide delivery — confidential, authenticated, considered.",
        canonical_path="/process.html",
        page_css=page_css,
        extra_jsonld=extra_jsonld,
    )

    steps = [
        ("01", "The <em>Private Briefing</em>",
         "<p>A confidential conversation &mdash; in person, by phone or by message &mdash; to understand what you are looking for. The reference, the year, the dial; the condition you are willing to accept; the budget you are comfortable with.</p><p>No mandate is taken until both sides are clear on what is being asked for.</p>"),
        ("02", "The <em>Mandate &amp; The Search</em>",
         "<p>Once briefed we agree the terms of the search in writing &mdash; scope, budget boundaries and our fee. From that point the search begins quietly across our network of trusted dealers, collectors and auction contacts.</p><p>You are kept informed at the cadence you prefer; weekly summaries, only-when-it-matters, or somewhere in between.</p>"),
        ("03", "<em>Vetting</em> &amp; Negotiation",
         "<p>Candidates are shortlisted only after they have been photographed, examined and discussed with the seller. We negotiate on your behalf and never disclose you as the buyer.</p><p>Pieces that do not meet the brief are quietly declined.</p>"),
        ("04", "Independent <em>Verification</em>",
         "<p>Authenticity, condition and documentation are independently established before a single piece reaches you. Where required we engage specialist watchmakers for additional verification of movement and case.</p><p>If we cannot stand behind a piece, we do not present it.</p>"),
        ("05", "<em>Escrow</em> &amp; Settlement",
         "<p>Funds are routed through escrow where appropriate. Invoices, customs documentation and provenance records are prepared in the name and form most useful to you.</p><p>Nothing moves until everyone is satisfied.</p>"),
        ("06", "<em>Delivery</em> &amp; Handover",
         "<p>Fully insured white-glove delivery worldwide &mdash; to your door, your office, your hotel, or your private aviation. We are present at handover whenever possible.</p><p>The relationship does not end here; many of our clients return for the next piece, or simply to keep us watching the market on their behalf.</p>"),
    ]

    steps_html = ""
    for num, title, content in steps:
        steps_html += (
            f'<article class="proc-step reveal">'
            f'<div class="proc-num">N&deg; {num}</div>'
            f'<h3>{title}</h3>'
            f'<div class="pd">{content}</div>'
            f'</article>\n'
        )

    body = r"""
""" + header(active='process') + r"""

<main id="main">

<section class="page-hero" aria-labelledby="proc-h1">
  <div class="grain"></div>
  <div class="wrap">
    <div class="eyebrow reveal">The Process</div>
    <h1 id="proc-h1" class="reveal">From <em>brief</em> to <em>wrist</em>.</h1>
    <p class="lead reveal">Six stages, considered and deliberate. The work is in what happens between them &mdash; the conversations, the verifications, the patience. We do those bits well so the rest feels easy.</p>
  </div>
</section>

<section class="proc-list">
  <div class="wrap">
""" + steps_html + r"""
  </div>
</section>

<section class="assure-sec" aria-labelledby="ass-h2">
  <div class="wrap">
    <div class="sec-head reveal">
      <div>
        <div class="eyebrow" style="margin-bottom:22px">Why Watchmans</div>
        <h2 id="ass-h2">The <em>assurances</em></h2>
      </div>
      <div class="sh-r">The standard of care expected by collectors and private clients who value their time and their privacy.</div>
    </div>
    <div class="assure reveal">
      <div><div class="ic">i.</div><h4>Absolute discretion</h4><p>Every engagement is confidential. Your name never enters the market without instruction.</p></div>
      <div><div class="ic">ii.</div><h4>Verified provenance</h4><p>Independent authentication and a documented history on every piece, without exception.</p></div>
      <div><div class="ic">iii.</div><h4>Aligned interest</h4><p>A transparent service from first call to final handover. We are engaged to find the right watch &mdash; never to move the wrong one.</p></div>
      <div><div class="ic">iv.</div><h4>Client satisfaction</h4><p>A relationship measured by outcome, not transaction. Most of our work arrives by quiet introduction from those we have served well.</p></div>
    </div>
  </div>
</section>

<section class="proc-cta">
  <div class="wrap reveal">
    <h2>Ready to <em>begin</em>?</h2>
    <p>A short message is enough to start the conversation. We will reply by email within one working day &mdash; usually the same day.</p>
    <a href="enquire.html" class="btn">Begin an Enquiry</a>
  </div>
</section>

""" + enquire_section() + r"""

</main>
""" + render_footer()

    return head_html + body


# ============================================================
# ENQUIRE PAGE (enquire.html)
# Hero + contact tiles + form
# ============================================================
def enquire_page_html():
    page_css = r"""
  .contact-tiles{padding:30px 0 80px}
  .contact-tiles .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
    background:var(--line);border:1px solid var(--line)}
  .contact-tiles .ct{background:var(--paper);padding:46px 32px;text-align:left;
    transition:.45s;display:flex;flex-direction:column;justify-content:space-between;min-height:230px}
  .contact-tiles .ct:hover{background:var(--paper-2);transform:translateY(-2px)}
  .contact-tiles .ct .ic{width:38px;height:38px;color:var(--bronze);margin-bottom:30px}
  .contact-tiles .ct .ic svg{width:38px;height:38px;stroke:currentColor;fill:none;stroke-width:1.1}
  .contact-tiles .ct h3{font-family:var(--serif);font-size:24px;font-style:italic;
    color:var(--ink);margin-bottom:8px;font-weight:300}
  .contact-tiles .ct .ct-val{font-size:14px;color:var(--ink-soft);margin-bottom:18px;
    word-break:break-word}
  .contact-tiles .ct .ct-cta{font-size:11px;letter-spacing:.22em;text-transform:uppercase;
    color:var(--bronze-deep);font-weight:600}
  @media(max-width:1080px){
    .contact-tiles .grid{grid-template-columns:1fr 1fr}
  }
  @media(max-width:560px){
    .contact-tiles .grid{grid-template-columns:1fr}
  }
"""

    extra_jsonld = {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Watchmans Global",
        "url": f"{SITE_URL}/enquire.html",
        "description": "Reach Watchmans Global to begin a private watch enquiry — WhatsApp, email, phone or Instagram.",
        "contactOption": ["TollFree", "HearingImpairedSupported"]
    }

    head_html = head(
        title="Begin an Enquiry — Get in Touch",
        description="Begin a private watch enquiry with Watchmans Global. WhatsApp, email, phone, or send a brief through our contact form — reply by email within one working day.",
        canonical_path="/enquire.html",
        page_css=page_css,
        extra_jsonld=extra_jsonld,
    )

    body = r"""
""" + header(active='enquire') + r"""

<main id="main">

<section class="page-hero" aria-labelledby="enq-h1">
  <div class="grain"></div>
  <div class="wrap">
    <div class="eyebrow reveal">Begin an Enquiry</div>
    <h1 id="enq-h1" class="reveal">Get in <em>touch</em>.</h1>
    <p class="lead reveal">Tell us the watch you are looking for &mdash; or simply say hello. We reply by email within one working day, usually the same day. For something more immediate, WhatsApp or call.</p>
  </div>
</section>

<section class="contact-tiles" aria-label="Direct contact options">
  <div class="wrap">
    <div class="grid reveal">
      <a class="ct" href=""" + '"' + WHATSAPP + '"' + r""" target="_blank" rel="noopener">
        <div>
          <div class="ic"><svg viewBox="0 0 24 24"><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.2-1.3c1.5.8 3.1 1.2 4.8 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2z"/><path d="M8 9c0-.8.7-1.5 1.5-1.5h.8L11 11l-.8 1.2c.6 1.4 1.8 2.5 3.2 3.1l1.1-.8 3.5.7c0 .8-.7 1.5-1.5 1.5C12.4 16.7 8 13.5 8 9z"/></svg></div>
          <h3>WhatsApp</h3>
          <div class="ct-val">Message us directly &mdash; fastest reply</div>
        </div>
        <div class="ct-cta">Open WhatsApp &rarr;</div>
      </a>
      <a class="ct" href="mailto:""" + EMAIL + r"""">
        <div>
          <div class="ic"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/></svg></div>
          <h3>Email</h3>
          <div class="ct-val">""" + EMAIL + r"""</div>
        </div>
        <div class="ct-cta">Send Email &rarr;</div>
      </a>
      <a class="ct" href=""" + '"tel:' + PHONE_INTL + '"' + r""">
        <div>
          <div class="ic"><svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.13.96.36 1.9.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0122 16.92z"/></svg></div>
          <h3>Phone</h3>
          <div class="ct-val">""" + PHONE + r"""</div>
        </div>
        <div class="ct-cta">Call Now &rarr;</div>
      </a>
      <a class="ct" href=""" + '"' + INSTAGRAM + '"' + r""" target="_blank" rel="noopener">
        <div>
          <div class="ic"><svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></div>
          <h3>Instagram</h3>
          <div class="ct-val">""" + INSTAGRAM_HANDLE + r"""</div>
        </div>
        <div class="ct-cta">Follow &rarr;</div>
      </a>
    </div>
  </div>
</section>

""" + enquire_section(compact=False) + r"""

</main>
""" + render_footer()

    return head_html + body


# ============================================================
# MAIN — write all pages + robots + sitemap + copy logo
# ============================================================
if __name__ == '__main__':
    os.makedirs(OUTDIR, exist_ok=True)

    # Copy logo (external = much smaller pages = better SEO)
    if os.path.exists(LOGO_SRC):
        shutil.copy(LOGO_SRC, os.path.join(OUTDIR, 'logo.png'))
        print(f"  ✓ Copied logo.png ({os.path.getsize(LOGO_SRC)} bytes)")
    else:
        print(f"  ⚠ Logo not found at {LOGO_SRC} — pages will reference missing logo.png")

    # Generate all pages
    pages = {
        'index.html':            home_html(),
        'collection.html':       collection_html(),
        'bespoke-sourcing.html': sourcing_html(),
        'process.html':          process_html(),
        'enquire.html':          enquire_page_html(),
    }
    for filename, html in pages.items():
        out_path = os.path.join(OUTDIR, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✓ Wrote {filename:24s} ({len(html):>7,} chars)")

    # robots.txt — tells crawlers what's allowed + where the sitemap is
    robots = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Sitemap: {SITE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTDIR, 'robots.txt'), 'w') as f:
        f.write(robots)
    print(f"  ✓ Wrote robots.txt")

    # sitemap.xml — lists all pages with priority hints for Google
    today = "2026-05-20"
    urls = [
        ('/', '1.0', 'weekly'),
        ('/collection.html', '0.9', 'daily'),
        ('/bespoke-sourcing.html', '0.85', 'monthly'),
        ('/process.html', '0.8', 'monthly'),
        ('/enquire.html', '0.85', 'monthly'),
    ]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path, priority, freq in urls:
        sitemap += f'  <url>\n    <loc>{SITE_URL}{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
    sitemap += '</urlset>\n'
    with open(os.path.join(OUTDIR, 'sitemap.xml'), 'w') as f:
        f.write(sitemap)
    print(f"  ✓ Wrote sitemap.xml")

    print("\n  Build complete.")
