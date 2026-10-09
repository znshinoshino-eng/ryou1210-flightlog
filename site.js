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
  var LANGS = ["en", "fr", "de", "es"];
  var LANG_NAMES = { en: "English", fr: "Français", de: "Deutsch", es: "Español" };
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
          areas: { tokyo: "Tokio", hakone: "Hakone y Fuji", kansai: "Kioto y Osaka", hokuriku: "Kanazawa y Alpes", japan: "Todo Japón" } }
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
      var words = (article.innerText || article.textContent).trim().split(/\s+/).length;
      var mins = Math.max(1, Math.round(words / 230));
      var info = el("div", { "class": "readinfo" });
      info.appendChild(el("span", null, mins + " " + T.min));
      var lm = new Date(document.lastModified);
      if (!isNaN(lm) && lm.getFullYear() > 2020) {
        info.appendChild(el("span", null, T.updated + " " + lm.toLocaleDateString(lang === "en" ? "en-US" : lang, { year: "numeric", month: "short", day: "numeric" })));
      }
      meta.insertAdjacentElement("afterend", info);
    }

    // 3. Affiliate note when the page has sponsored links
    var firstH2 = h2s[0];
    if (article.querySelector('a[rel~="sponsored"]') && firstH2) {
      var note = el("p", { "class": "aff-note" });
      note.appendChild(document.createTextNode(T.aff));
      var more = el("a", { href: ROOT + "about.html" }, T.affMore);
      note.appendChild(more);
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
    var cards = Array.prototype.slice.call(listEl.querySelectorAll(".post-card"));
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
      listEl.classList.toggle("filtered", filtered);
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
      listEl.parentNode.insertBefore(panel, listEl);
      listEl.parentNode.insertBefore(empty, listEl.nextSibling);
      apply();
    }
  }
})();
