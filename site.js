/* Flightlog Japan — reading aids added on top of plain article HTML.
   Every article stays fully readable without this script; it only adds:
   breadcrumb, reading time + last-updated line, "In this guide" contents,
   affiliate note, "Keep reading" links, and category filters on the top page. */
(function () {
  "use strict";


  // Page view counting (GoatCounter: no cookies, no personal data)
  if (!/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && !document.querySelector("script[data-goatcounter]")) {
    var gc = document.createElement("script");
    gc.async = true;
    gc.src = "https://gc.zgo.at/count.js";
    gc.setAttribute("data-goatcounter", "https://shino.goatcounter.com/count");
    document.head.appendChild(gc);
  }


  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text != null) n.textContent = text;
    return n;
  }

  // ---- Language ----------------------------------------------------------
  var LANGS = ["en", "fr", "de", "es", "th"];
  var LANG_NAMES = { en: "English", fr: "Français", de: "Deutsch", es: "Español", th: "ไทย" };
  var lang = (document.documentElement.lang || "en").slice(0, 2);
  if (LANGS.indexOf(lang) < 0) lang = "en";
  var T = {
    en: { articles: "Articles", min: "min read", updated: "Updated", aff: "This guide contains affiliate links. Booking through them costs you nothing extra. ", affMore: "How we choose what to link", toc: "In this guide", keep: "Keep reading", area: "Area", topic: "Topic", all: "All", guide: "guide", guides: "guides", none: "No guides here yet. More are on the way.", language: "Language",
          areas: { tokyo: "Tokyo", hakone: "Hakone & Fuji", kansai: "Kyoto & Osaka", hokuriku: "Kanazawa & Alps", japan: "Nationwide" } },
    fr: { articles: "Articles", min: "min de lecture", updated: "Mis à jour le", aff: "Ce guide contient des liens affiliés. Réserver via ces liens ne vous coûte rien de plus. ", affMore: "Comment nous choisissons nos liens", toc: "Dans ce guide", keep: "À lire aussi", area: "Région", topic: "Thème", all: "Tout", guide: "guide", guides: "guides", none: "Pas encore de guide ici. D'autres arrivent bientôt.", language: "Langue",
          areas: { tokyo: "Tokyo", hakone: "Hakone et Fuji", kansai: "Kyoto et Osaka", hokuriku: "Kanazawa et Alpes", japan: "Tout le Japon" } },
    de: { articles: "Artikel", min: "Min. Lesezeit", updated: "Aktualisiert am", aff: "Dieser Guide enthält Affiliate-Links. Wenn du darüber buchst, kostet es dich nichts extra. ", affMore: "Wie wir Links auswählen", toc: "In diesem Guide", keep: "Weiterlesen", area: "Region", topic: "Thema", all: "Alle", guide: "Guide", guides: "Guides", none: "Hier gibt es noch keine Guides. Weitere folgen bald.", language: "Sprache",
          areas: { tokyo: "Tokio", hakone: "Hakone & Fuji", kansai: "Kyoto & Osaka", hokuriku: "Kanazawa & Alpen", japan: "Ganz Japan" } },
    es: { articles: "Artículos", min: "min de lectura", updated: "Actualizado el", aff: "Esta guía contiene enlaces de afiliado. Reservar a través de ellos no te cuesta nada extra. ", affMore: "Cómo elegimos los enlaces", toc: "En esta guía", keep: "Sigue leyendo", area: "Zona", topic: "Tema", all: "Todo", guide: "guía", guides: "guías", none: "Todavía no hay guías aquí. Pronto habrá más.", language: "Idioma",
          areas: { tokyo: "Tokio", hakone: "Hakone y Fuji", kansai: "Kioto y Osaka", hokuriku: "Kanazawa y Alpes", japan: "Todo Japón" } },
    th: { articles: "บทความ", min: "นาทีในการอ่าน", updated: "อัปเดตเมื่อ", aff: "คู่มือนี้มีลิงก์พันธมิตร การจองผ่านลิงก์เหล่านี้ไม่มีค่าใช้จ่ายเพิ่มเติม ", affMore: "เราเลือกลิงก์อย่างไร", toc: "ในคู่มือนี้", keep: "อ่านต่อ", area: "พื้นที่", topic: "หัวข้อ", all: "ทั้งหมด", guide: "คู่มือ", guides: "คู่มือ", none: "ยังไม่มีคู่มือในหมวดนี้ เร็ว ๆ นี้จะมีเพิ่ม", language: "ภาษา",
          areas: { tokyo: "โตเกียว", hakone: "ฮาโกเนะและฟูจิ", kansai: "เกียวโตและโอซาก้า", hokuriku: "คานาซาวะและแอลป์", japan: "ทั่วญี่ปุ่น" } }
  }[lang];

  // Wide tables on phones: say they can be swiped sideways (only while they overflow)
  (function () {
    var SWIPE = { en: "Swipe the table sideways to see all columns", fr: "Faites glisser le tableau pour voir toutes les colonnes", de: "Tabelle seitlich wischen, um alle Spalten zu sehen", es: "Desliza la tabla para ver todas las columnas", th: "ปัดตารางไปด้านข้างเพื่อดูทุกคอลัมน์" }[lang];
    var tables = Array.prototype.slice.call(document.querySelectorAll("article.post table"));
    if (!tables.length) return;
    var hints = tables.map(function (t) {
      var h = el("p", { "class": "table-hint", "aria-hidden": "true" }, SWIPE + " →");
      t.parentNode.insertBefore(h, t);
      return h;
    });
    function check() {
      tables.forEach(function (t, i) { hints[i].hidden = t.scrollWidth <= t.clientWidth + 2; });
    }
    check();
    window.addEventListener("resize", check);
    window.addEventListener("load", check);
  })();

  // Why we link to Klook (shown on pages with Klook links)
  var K = {
    "en": {
      "title": "Why we link to Klook",
      "points": [
        "You can book in English and pay in your own currency, even when the operator only sells in Japanese or at a station counter.",
        "Most bookings are confirmed instantly, with a QR code or voucher on your phone.",
        "Prices are usually the same as the official price or close to it. We note the date we checked.",
        "When the station or the official site is just as easy or cheaper, we say so."
      ],
      "more": "More about how we choose links"
    },
    "fr": {
      "title": "Pourquoi nous recommandons Klook",
      "points": [
        "Vous pouvez réserver en français ou en anglais et payer dans votre devise, même quand l'opérateur ne vend qu'en japonais ou au guichet.",
        "La plupart des réservations sont confirmées immédiatement, avec un QR code ou un bon sur votre téléphone.",
        "Les prix sont généralement identiques ou proches du prix officiel. Nous indiquons la date de vérification.",
        "Quand la gare ou le site officiel est aussi simple ou moins cher, nous le disons."
      ],
      "more": "En savoir plus sur le choix de nos liens"
    },
    "de": {
      "title": "Warum wir Klook empfehlen",
      "points": [
        "Du kannst auf Deutsch oder Englisch buchen und in deiner Währung zahlen, auch wenn der Anbieter nur auf Japanisch oder am Schalter verkauft.",
        "Die meisten Buchungen werden sofort bestätigt, mit QR-Code oder Voucher auf dem Handy.",
        "Die Preise entsprechen meist dem offiziellen Preis oder liegen nah daran. Wir nennen das Datum unserer Prüfung.",
        "Wenn der Bahnhof oder die offizielle Website genauso einfach oder günstiger ist, sagen wir das."
      ],
      "more": "Mehr dazu, wie wir Links auswählen"
    },
    "es": {
      "title": "Por qué recomendamos Klook",
      "points": [
        "Puedes reservar en español o inglés y pagar en tu moneda, incluso cuando el operador solo vende en japonés o en la taquilla.",
        "La mayoría de las reservas se confirman al instante, con un código QR o un bono en tu móvil.",
        "Los precios suelen ser iguales o muy parecidos al precio oficial. Indicamos la fecha en que los revisamos.",
        "Cuando la estación o la web oficial es igual de fácil o más barata, lo decimos."
      ],
      "more": "Más sobre cómo elegimos los enlaces"
    },
    "th": {
      "title": "ทำไมเราแนะนำ Klook",
      "points": [
        "จองเป็นภาษาไทยหรืออังกฤษ และจ่ายด้วยสกุลเงินของคุณได้ แม้ผู้ให้บริการจะขายเป็นภาษาญี่ปุ่นหรือที่เคาน์เตอร์เท่านั้น",
        "การจองส่วนใหญ่ได้รับการยืนยันทันที พร้อม QR code หรือวอเชอร์ในมือถือ",
        "ราคามักเท่ากับหรือใกล้เคียงราคาทางการ เราระบุวันที่ที่ตรวจสอบราคาไว้",
        "ถ้าซื้อที่สถานีหรือเว็บไซต์ทางการง่ายพอกันหรือถูกกว่า เราจะบอกไว้ตรง ๆ"
      ],
      "more": "อ่านเพิ่มเติมว่าเราเลือกลิงก์อย่างไร"
    }
  }[lang];

  // Site root, e.g. "/ryou1210-flightlog/", worked out from this page's path
  var segs = location.pathname.split("/");
  segs.pop();                                   // file name
  if (segs[segs.length - 1] === "articles") segs.pop();
  if (LANGS.indexOf(segs[segs.length - 1]) > 0) segs.pop();
  var ROOT = segs.join("/") + "/";

  // Language switcher in the header: uses hreflang links when the page is translated,
  // otherwise sends readers to that language's home page.
  (function () {
    var nav = document.querySelector(".site-nav");
    if (!nav) return;
    var alts = {};
    Array.prototype.forEach.call(document.querySelectorAll('link[rel="alternate"][hreflang]'), function (l) {
      alts[l.getAttribute("hreflang")] = l.getAttribute("href");
    });
    var box = el("details", { "class": "lang-switch" });
    var sum = el("summary", { "aria-label": T.language }, lang.toUpperCase());
    box.appendChild(sum);
    var menu = el("div", { "class": "lang-menu" });
    LANGS.forEach(function (l) {
      var href = alts[l] || (ROOT + (l === "en" ? "" : l + "/"));
      var a = el("a", { href: href, hreflang: l, lang: l }, LANG_NAMES[l]);
      if (l === lang) a.setAttribute("aria-current", "true");
      menu.appendChild(a);
    });
    box.appendChild(menu);
    document.addEventListener("click", function (ev) { if (!box.contains(ev.target)) box.removeAttribute("open"); });
    nav.appendChild(box);
  })();

  var article = document.querySelector("article.post");
  var isArticle = !!(article && /\/articles\//.test(location.pathname));

  function slugify(s) {
    return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "section";
  }

  if (isArticle) {
    var h1 = article.querySelector("h1");
    var cat = article.querySelector(".cat");
    var meta = article.querySelector(".meta");
    var h2s = Array.prototype.slice.call(article.querySelectorAll("h2"));

    // 1. Breadcrumb: Articles › Category
    if (h1) {
      var bc = el("nav", { "class": "crumbs", "aria-label": "Breadcrumb" });
      var home = el("a", { href: "../index.html" }, T.articles);
      bc.appendChild(home);
      if (cat) {
        bc.appendChild(el("span", { "aria-hidden": "true" }, "›"));
        bc.appendChild(el("span", null, cat.textContent.trim()));
      }
      article.insertBefore(bc, article.firstChild);
    }

    // 2. Reading time and last updated
    if (meta) {
      var bodyText = (article.innerText || article.textContent).trim();
      // Thai has no spaces between words, so estimate from characters instead
      var words = lang === "th" ? Math.round(bodyText.replace(/\s+/g, "").length / 6) : bodyText.split(/\s+/).length;
      var mins = Math.max(1, Math.round(words / 230));
      var info = el("div", { "class": "readinfo" });
      info.appendChild(el("span", null, mins + " " + T.min));
      var lm = new Date(document.lastModified);
      if (!isNaN(lm) && lm.getFullYear() > 2020) {
        info.appendChild(el("span", null, T.updated + " " + lm.toLocaleDateString(lang === "en" ? "en-US" : lang, { year: "numeric", month: "short", day: "numeric" })));
      }
      meta.insertAdjacentElement("afterend", info);
    }

    // 3. Affiliate note when the page has sponsored links, with a short "Why Klook?" explanation
    var firstH2 = h2s[0];
    if (article.querySelector('a[rel~="sponsored"]') && firstH2) {
      var note = el("div", { "class": "aff-note" });
      var line = el("p");
      line.appendChild(document.createTextNode(T.aff));
      note.appendChild(line);
      if (article.querySelector('a[href*="klook.com"]')) {
        var why = el("details", { "class": "why-klook" });
        why.appendChild(el("summary", null, K.title));
        var ul = el("ul");
        K.points.forEach(function (pt) { ul.appendChild(el("li", null, pt)); });
        why.appendChild(ul);
        var whyMore = el("p");
        whyMore.appendChild(el("a", { href: ROOT + "about.html#why-klook" }, K.more));
        why.appendChild(whyMore);
        note.appendChild(why);
      } else {
        line.appendChild(el("a", { href: ROOT + "about.html" }, T.affMore));
      }
      firstH2.parentNode.insertBefore(note, firstH2);
    }

    // 4. Contents box built from the h2 headings
    if (h2s.length >= 3) {
      var box = el("details", { "class": "toc", open: "" });
      box.appendChild(el("summary", null, T.toc));
      var ul = el("ul");
      var used = {};
      h2s.forEach(function (h) {
        var id = h.id || slugify(h.textContent);
        while (used[id]) id += "-2";
        used[id] = true;
        h.id = id;
        var li = el("li");
        li.appendChild(el("a", { href: "#" + id }, h.textContent.trim()));
        ul.appendChild(li);
      });
      box.appendChild(ul);
      var anchor = article.querySelector(".aff-note") || firstH2;
      // put the contents right after the opening paragraph(s), before the first section
      anchor.parentNode.insertBefore(box, anchor);
      if (window.matchMedia && window.matchMedia("(max-width: 720px)").matches) box.removeAttribute("open");
    }

    // 5. Keep reading: three other guides, taken from the top page
    var back = article.querySelector(".back-link");
    if (back && window.fetch) {
      fetch("../index.html", { cache: "no-cache" }).then(function (r) { return r.ok ? r.text() : ""; }).then(function (html) {
        if (!html) return;
        var doc = new DOMParser().parseFromString(html, "text/html");
        var here = location.pathname.split("/").pop();
        var cards = Array.prototype.slice.call(doc.querySelectorAll("a.post-card")).filter(function (a) {
          return a.getAttribute("href").split("/").pop() !== here;
        });
        var myCat = cat ? cat.textContent.trim() : "";
        cards.sort(function (a, b) {
          var ca = (a.querySelector(".cat") || {}).textContent === myCat ? 0 : 1;
          var cb = (b.querySelector(".cat") || {}).textContent === myCat ? 0 : 1;
          return ca - cb;
        });
        cards = cards.slice(0, 3);
        if (!cards.length) return;
        var sec = el("section", { "class": "related", "aria-labelledby": "related-h" });
        sec.appendChild(el("h2", { id: "related-h" }, T.keep));
        var list = el("div", { "class": "related-list" });
        cards.forEach(function (a) {
          var link = el("a", { "class": "related-card", href: "../" + a.getAttribute("href") });
          var img = a.querySelector("img.thumb");
          if (img) link.appendChild(el("img", { src: img.getAttribute("src"), alt: "", loading: "lazy", width: "720", height: "405" }));
          var c = a.querySelector(".cat");
          if (c) link.appendChild(el("span", { "class": "rcat" }, c.textContent));
          link.appendChild(el("span", { "class": "rtitle" }, (a.querySelector("h2") || a).textContent.trim()));
          list.appendChild(link);
        });
        sec.appendChild(list);
        back.parentNode.insertBefore(sec, back);
      }).catch(function () {});
    }
  }

  // Top page: filter by area and by topic.
  // Cards carry data-region="tokyo kansai ..."; "japan" means nationwide and shows under every area.
  var AREAS = [
    ["tokyo", "Tokyo"],
    ["hakone", "Hakone & Fuji"],
    ["kansai", "Kyoto & Osaka"],
    ["hokuriku", "Kanazawa & Alps"],
    ["japan", "Nationwide"]
  ];
  var listEl = document.querySelector(".post-list");
  if (listEl && !isArticle) {
    var lists = Array.prototype.slice.call(document.querySelectorAll(".post-list"));
    var sections = Array.prototype.slice.call(document.querySelectorAll(".post-section"));
    var cards = Array.prototype.slice.call(document.querySelectorAll(".post-list .post-card"));
    var catOf = function (c) { return ((c.querySelector(".cat") || {}).textContent || "").trim(); };
    var regionsOf = function (c) { return (c.getAttribute("data-region") || "japan").split(/\s+/); };
    var cats = [];
    cards.forEach(function (c) { var t = catOf(c); if (t && cats.indexOf(t) < 0) cats.push(t); });
    var present = {};
    cards.forEach(function (c) { regionsOf(c).forEach(function (r) { present[r] = true; }); });
    var areas = AREAS.filter(function (a) { return present[a[0]]; });

    var params = new URLSearchParams(location.search);
    var state = { area: params.get("area") || "", topic: "" };
    if (!areas.some(function (a) { return a[0] === state.area; })) state.area = "";

    var panel = el("div", { "class": "filter-panel" });
    var count = el("p", { "class": "filter-count", "aria-live": "polite" });
    var empty = el("p", { "class": "filter-empty", hidden: "" }, T.none);

    function apply() {
      var shown = 0;
      cards.forEach(function (c) {
        var rs = regionsOf(c);
        var okArea = !state.area || rs.indexOf(state.area) >= 0 || rs.indexOf("japan") >= 0;
        var okTopic = !state.topic || catOf(c) === state.topic;
        c.hidden = !(okArea && okTopic);
        if (!c.hidden) shown++;
      });
      var filtered = !!(state.area || state.topic);
      lists.forEach(function (l) { l.classList.toggle("filtered", filtered); });
      // hide a whole section when none of its guides match
      sections.forEach(function (sec) { sec.hidden = !sec.querySelector(".post-card:not([hidden])"); });
      count.textContent = filtered ? shown + " " + (shown === 1 ? T.guide : T.guides) : "";
      count.hidden = !filtered;
      empty.hidden = shown > 0;
      var url = new URL(location.href);
      if (state.area) url.searchParams.set("area", state.area); else url.searchParams.delete("area");
      history.replaceState(null, "", url);
    }

    function row(label, aria, options, key) {
      var r = el("div", { "class": "filter-row" });
      r.appendChild(el("span", { "class": "filter-label" }, label));
      var bar = el("div", { "class": "filters", role: "toolbar", "aria-label": aria });
      options.forEach(function (o) {
        var b = el("button", { type: "button", "aria-pressed": state[key] === o[0] ? "true" : "false" }, o[1]);
        b.addEventListener("click", function () {
          state[key] = o[0];
          Array.prototype.forEach.call(bar.children, function (x) { x.setAttribute("aria-pressed", "false"); });
          b.setAttribute("aria-pressed", "true");
          apply();
        });
        bar.appendChild(b);
      });
      r.appendChild(bar);
      return r;
    }

    if (areas.length > 1) panel.appendChild(row(T.area, "Filter guides by area", [["", T.all]].concat(areas.map(function (a) { return [a[0], T.areas[a[0]] || a[1]]; })), "area"));
    if (cats.length > 1) panel.appendChild(row(T.topic, "Filter guides by topic", [["", T.all]].concat(cats.map(function (c) { return [c, c]; })), "topic"));
    if (panel.children.length) {
      panel.appendChild(count);
      var first = sections[0] || listEl;
      first.parentNode.insertBefore(panel, first);
      var last = sections.length ? sections[sections.length - 1] : listEl;
      last.parentNode.insertBefore(empty, last.nextSibling);
      apply();
    }
  }
})();

/* Highlight the guide-section bar: on the top page, the section in view;
   on an article, the section that lists it. */
(function () {
  "use strict";
  var bar = document.querySelector(".section-nav");
  if (!bar) return;
  var links = Array.prototype.slice.call(bar.querySelectorAll("a"));
  function mark(id) {
    links.forEach(function (a) {
      var on = a.getAttribute("href").split("#")[1] === id;
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
  }
  var sections = Array.prototype.slice.call(document.querySelectorAll(".post-section"));
  if (sections.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function (s) { io.observe(s); });
    return;
  }
  if (/\/articles\//.test(location.pathname) && window.fetch) {
    var here = location.pathname.split("/").pop();
    fetch("../index.html").then(function (r) { return r.ok ? r.text() : ""; }).then(function (html) {
      if (!html) return;
      var doc = new DOMParser().parseFromString(html, "text/html");
      var card = doc.querySelector('.post-section a.post-card[href$="' + here + '"]');
      var sec = card && card.closest(".post-section");
      if (sec) mark(sec.id);
    }).catch(function () {});
  }
})();
