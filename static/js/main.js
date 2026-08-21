/* =========================================================================
   SILEX ELEVATOR — front-end interactions
   Smooth, silent, smart micro-interactions (logolift-inspired)
   ========================================================================= */
(function () {
  "use strict";

  var doc = document;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Elevator intro · zoom into the logo lift, doors open onto the site */
  (function () {
    var intro = doc.querySelector("[data-lift-intro]");
    if (!intro) return;

    // Only play once per browser session so navigation doesn't replay it.
    var already = false;
    try { already = sessionStorage.getItem("silexLiftIntro") === "1"; } catch (e) {}

    function finish() {
      intro.classList.add("is-done");
      doc.body.classList.remove("lift-lock");
      window.setTimeout(function () { intro.classList.add("is-off"); }, 750);
    }

    if (already) { intro.classList.add("is-off"); return; }
    try { sessionStorage.setItem("silexLiftIntro", "1"); } catch (e) {}

    doc.body.classList.add("lift-lock");
    var floorEl = intro.querySelector("[data-lift-floor]");

    if (reduceMotion) {
      intro.classList.add("is-in", "is-doors");
      window.setTimeout(function () { intro.classList.add("is-open"); }, 200);
      window.setTimeout(finish, 1200);
      return;
    }

    // 1) fade the logo in, 2) zoom into the lift, 3) hand over to steel doors,
    // 4) tick the floor number, 5) part the doors onto the page, 6) fade out.
    window.setTimeout(function () { intro.classList.add("is-in"); }, 60);
    window.setTimeout(function () { intro.classList.add("is-zoom"); }, 560);
    window.setTimeout(function () { intro.classList.add("is-doors"); }, 1650);

    // brief floor tick while doors are closed
    var floors = ["G", "1", "2"];
    var fi = 0;
    window.setTimeout(function tick() {
      if (floorEl) floorEl.textContent = floors[fi];
      fi++;
      if (fi < floors.length) window.setTimeout(tick, 260);
    }, 1850);

    window.setTimeout(function () { intro.classList.add("is-open"); }, 2500);
    window.setTimeout(finish, 3850);
  })();

  /* ---- Sticky navbar shadow --------------------------------------------- */
  var nav = doc.querySelector(".nav");
  function onScroll() {
    if (nav) nav.classList.toggle("is-stuck", window.scrollY > 20);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---- Mobile menu toggle ------------------------------------------------ */
  var toggle = doc.querySelector(".nav__toggle");
  var links = doc.querySelector(".nav__links");
  var scrim = doc.getElementById("navScrim");
  if (toggle && links) {
    function setMenu(open) {
      links.classList.toggle("open", open);
      if (scrim) scrim.classList.toggle("open", open);
      doc.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) links.scrollTop = 0;
    }

    toggle.addEventListener("click", function () {
      setMenu(!links.classList.contains("open"));
    });
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        setMenu(false);
      }
    });
    if (scrim) scrim.addEventListener("click", function () { setMenu(false); });

    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  /* ---- Nav dropdown accordions (mobile drawer only) --------------------- */
  doc.querySelectorAll(".drop-toggle").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (window.innerWidth > 980) return; // desktop uses hover flyouts
      e.preventDefault();
      var parent = btn.closest(".has-drop");
      if (!parent) return;
      var isOpen = parent.classList.contains("open");
      doc.querySelectorAll(".has-drop.open").forEach(function (o) {
        if (o !== parent) o.classList.remove("open");
      });
      parent.classList.toggle("open", !isOpen);
    });
  });

  /* ---- Glass card pointer spotlight ------------------------------------- */
  if (!reduceMotion && window.matchMedia("(pointer:fine)").matches) {
    doc.querySelectorAll(".pcard, .card").forEach(function (el) {
      el.addEventListener("pointermove", function (ev) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", ((ev.clientX - r.left) / r.width * 100) + "%");
        el.style.setProperty("--my", ((ev.clientY - r.top) / r.height * 100) + "%");
      });
    });
  }

  /* ---- Cookie consent ---------------------------------------------------- */
  var cookieBar = doc.getElementById("cookieBar");
  if (cookieBar) {
    var KEY = "silex_cookie_consent";

    function readConsent() {
      // Prefer a first-party cookie (persists even where localStorage is blocked).
      var m = doc.cookie.match(/(?:^|;\s*)silex_cookie_consent=([^;]+)/);
      if (m) return m[1];
      try { return localStorage.getItem(KEY); } catch (e) { return null; }
    }

    function writeConsent(value) {
      var oneYear = 60 * 60 * 24 * 365;
      doc.cookie = KEY + "=" + value + ";path=/;max-age=" + oneYear + ";SameSite=Lax";
      try { localStorage.setItem(KEY, value); } catch (e) {}
    }

    if (!readConsent()) {
      cookieBar.hidden = false;
      var close = function (value) {
        writeConsent(value);
        cookieBar.hidden = true;
      };
      var accept = doc.getElementById("cookieAccept");
      var decline = doc.getElementById("cookieDecline");
      if (accept) accept.addEventListener("click", function () { close("accepted"); });
      if (decline) decline.addEventListener("click", function () { close("declined"); });
    }
  }

  /* ---- Reveal on scroll (with stagger) ---------------------------------- */
  var reveals = doc.querySelectorAll(".reveal");
  if (reduceMotion) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -60px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }
  /* ---- Horizontal carousels (auto-float + arrows) ----------------------- */
  doc.querySelectorAll("[data-carousel]").forEach(function (car) {
    var track = car.querySelector("[data-carousel-track]");
    if (!track) return;
    var prev = car.querySelector("[data-carousel-prev]");
    var next = car.querySelector("[data-carousel-next]");
    var dir = 1;          // 1 = drift content leftwards (scrollLeft++)
    var paused = false;
    var speed = 0.45;     // px per frame
    var pos = track.scrollLeft;

    function maxScroll() { return track.scrollWidth - track.clientWidth; }

    function updateArrows() {
      var x = track.scrollLeft, max = maxScroll();
      if (prev) prev.disabled = x <= 2;
      if (next) next.disabled = x >= max - 2;
    }

    function step() {
      if (!paused && !reduceMotion && maxScroll() > 4) {
        var max = maxScroll();
        pos += speed * dir;
        if (pos >= max) { pos = max; dir = -1; }   // bounce at the right end
        else if (pos <= 0) { pos = 0; dir = 1; }   // bounce at the left end
        track.scrollLeft = pos;
      } else {
        pos = track.scrollLeft; // keep in sync during manual/paused scrolling
      }
      updateArrows();
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);

    function pause() { paused = true; car.classList.add("is-touched"); }
    function resume() { paused = false; car.classList.remove("is-touched"); }

    car.addEventListener("pointerenter", pause);
    car.addEventListener("pointerleave", resume);
    car.addEventListener("touchstart", pause, { passive: true });
    car.addEventListener("focusin", pause);
    car.addEventListener("focusout", resume);

    function scrollByCard(d) {
      var card = track.querySelector(".carousel__item");
      var amt = card ? card.getBoundingClientRect().width + 22 : track.clientWidth * 0.8;
      track.scrollBy({ left: d * amt, behavior: "smooth" });
    }
    if (prev) prev.addEventListener("click", function () { pause(); scrollByCard(-1); });
    if (next) next.addEventListener("click", function () { pause(); scrollByCard(1); });
    track.addEventListener("scroll", updateArrows, { passive: true });
    updateArrows();
  });

  /* ---- Full-width panel scroller (Showroom · Blog · Stay Lifted) -------- */
  doc.querySelectorAll("[data-panels]").forEach(function (root) {
    var track = root.querySelector("[data-panels-track]");
    if (!track) return;
    var prev = root.querySelector("[data-panels-prev]");
    var next = root.querySelector("[data-panels-next]");
    var dotsWrap = root.parentElement.querySelector("[data-panels-dots]");
    var panels = Array.prototype.slice.call(track.children);
    var dots = [];

    if (dotsWrap) {
      panels.forEach(function (p, i) {
        var b = doc.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", "Go to section " + (i + 1));
        b.addEventListener("click", function () { goTo(i); });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }

    function current() {
      return Math.round(track.scrollLeft / track.clientWidth);
    }
    function syncHeight() {
      var p = panels[current()];
      if (p) track.style.height = p.offsetHeight + "px";
    }
    function goTo(i) {
      i = Math.max(0, Math.min(panels.length - 1, i));
      track.scrollTo({ left: i * track.clientWidth, behavior: "smooth" });
    }
    function update() {
      var x = track.scrollLeft, max = track.scrollWidth - track.clientWidth;
      if (prev) prev.disabled = x <= 2;
      if (next) next.disabled = x >= max - 2;
      var idx = current();
      dots.forEach(function (d, i) { d.classList.toggle("is-active", i === idx); });
      syncHeight();
    }

    if (prev) prev.addEventListener("click", function () { goTo(current() - 1); });
    if (next) next.addEventListener("click", function () { goTo(current() + 1); });
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    window.addEventListener("load", syncHeight);
    update();
  });

  /* ---- Virtual Showroom · 360° rotating gallery room ------------------- */
  (function () {
    var modal = doc.querySelector("[data-vsr-modal]");
    if (!modal) return;
    var ring = modal.querySelector("[data-vsr-ring]");
    var cells = Array.prototype.slice.call(ring.querySelectorAll(".vsr-cell"));
    var n = cells.length;
    if (!n) return;

    var theta = 360 / n;
    var current = 0;
    var radius = 480;
    var autoTimer = null;

    var openers = doc.querySelectorAll("[data-vsr-open]");
    var closers = modal.querySelectorAll("[data-vsr-close]");
    var prevBtn = modal.querySelector("[data-vsr-prev]");
    var nextBtn = modal.querySelector("[data-vsr-next]");
    var dotsWrap = modal.querySelector("[data-vsr-dots]");
    var elPlace = modal.querySelector("[data-vsr-place]");
    var elLift = modal.querySelector("[data-vsr-lift]");
    var elNote = modal.querySelector("[data-vsr-note]");
    var elIndex = modal.querySelector("[data-vsr-index]");
    var stage = modal.querySelector("[data-vsr-stage]");

    var dots = [];
    cells.forEach(function (c, i) {
      var b = doc.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Go to " + (c.getAttribute("data-place") || "room " + (i + 1)));
      b.addEventListener("click", function () { goTo(i); resetAuto(); });
      dotsWrap.appendChild(b);
      dots.push(b);
    });

    function computeRadius() {
      var w = cells[0].getBoundingClientRect().width || 340;
      radius = Math.round((w / 2) / Math.tan(Math.PI / n)) + 30;
      ring.style.setProperty("--theta", theta + "deg");
      ring.style.setProperty("--radius", radius + "px");
    }

    function render() {
      ring.style.transform = "translateZ(" + (-radius) + "px) rotateY(" + (-theta * current) + "deg)";
      cells.forEach(function (c, i) {
        var d = (i - current + n) % n;
        d = Math.min(d, n - d);
        c.classList.toggle("is-side", d === 1);
        c.classList.toggle("is-far", d > 1);
      });
      var cur = cells[current];
      if (elPlace) elPlace.textContent = cur.getAttribute("data-place") || "";
      if (elLift) elLift.textContent = cur.getAttribute("data-lift") || "";
      if (elNote) elNote.textContent = cur.getAttribute("data-note") || "";
      if (elIndex) elIndex.textContent = current + 1;
      dots.forEach(function (d, i) { d.classList.toggle("is-active", i === current); });
    }

    function goTo(i) { current = ((i % n) + n) % n; render(); }
    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    function startAuto() {
      stopAuto();
      if (reduceMotion) return;
      autoTimer = window.setInterval(next, 4200);
    }
    function stopAuto() { if (autoTimer) { window.clearInterval(autoTimer); autoTimer = null; } }
    function resetAuto() { startAuto(); }

    function open() {
      modal.hidden = false;
      computeRadius();
      render();
      void modal.offsetWidth;
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
      doc.body.style.overflow = "hidden";
      startAuto();
    }
    function close() {
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
      doc.body.style.overflow = "";
      stopAuto();
      window.setTimeout(function () { modal.hidden = true; }, 350);
    }

    openers.forEach(function (o) { o.addEventListener("click", open); });
    closers.forEach(function (c) { c.addEventListener("click", close); });
    if (prevBtn) prevBtn.addEventListener("click", function () { prev(); resetAuto(); });
    if (nextBtn) nextBtn.addEventListener("click", function () { next(); resetAuto(); });
    if (stage) {
      stage.addEventListener("pointerenter", stopAuto);
      stage.addEventListener("pointerleave", function () {
        if (modal.classList.contains("is-open")) startAuto();
      });
    }

    /* ---- 360° panorama viewer (drag to look around, Street-View style) --- */
    var pano = doc.querySelector("[data-pano]");
    var pImg = pano && pano.querySelector("[data-pano-img]");
    var pStage = pano && pano.querySelector("[data-pano-stage]");
    var pPlace = pano && pano.querySelector("[data-pano-place]");
    var pHint = pano && pano.querySelector("[data-pano-grabhint]");
    var pZoomIn = pano && pano.querySelector("[data-pano-zoomin]");
    var pZoomOut = pano && pano.querySelector("[data-pano-zoomout]");
    var ps = { x: 0, y: 0, scale: 1.5, vx: 0, vy: 0, dragging: false, lx: 0, ly: 0,
               raf: null, drift: true, dir: -1, hintTimer: null };

    function panoBounds() {
      var sw = pStage.clientWidth, sh = pStage.clientHeight;
      var iw = pImg.clientWidth * ps.scale, ih = pImg.clientHeight * ps.scale;
      return { mx: Math.max(0, (iw - sw) / 2), my: Math.max(0, (ih - sh) / 2) };
    }
    function panoApply() {
      var b = panoBounds();
      ps.x = Math.max(-b.mx, Math.min(b.mx, ps.x));
      ps.y = Math.max(-b.my, Math.min(b.my, ps.y));
      pImg.style.transform = "translate(-50%,-50%) translate(" + ps.x.toFixed(1) + "px," +
        ps.y.toFixed(1) + "px) scale(" + ps.scale + ")";
    }
    function panoLoop() {
      if (!ps.dragging) {
        if (ps.drift && !reduceMotion) {
          var b = panoBounds();
          ps.x += ps.dir * 0.3;
          if (ps.x <= -b.mx) ps.dir = 1; else if (ps.x >= b.mx) ps.dir = -1;
        } else {
          ps.vx *= 0.93; ps.vy *= 0.93;
          ps.x += ps.vx; ps.y += ps.vy;
          if (Math.abs(ps.vx) < 0.04) ps.vx = 0;
          if (Math.abs(ps.vy) < 0.04) ps.vy = 0;
        }
      }
      panoApply();
      ps.raf = requestAnimationFrame(panoLoop);
    }
    function panoZoom(d) { ps.scale = Math.min(2.6, Math.max(1, ps.scale + d)); panoApply(); }

    function openPano(i) {
      var c = cells[i];
      if (!c || !pano) return;
      stopAuto();
      pImg.src = c.getAttribute("data-photo") || c.querySelector("img").src;
      if (pPlace) pPlace.textContent = c.getAttribute("data-place") || "";
      ps.x = 0; ps.y = 0; ps.scale = 1.5; ps.vx = 0; ps.vy = 0; ps.drift = true; ps.dir = -1;
      if (pHint) pHint.classList.remove("is-hidden");
      if (ps.hintTimer) window.clearTimeout(ps.hintTimer);
      ps.hintTimer = window.setTimeout(function () { if (pHint) pHint.classList.add("is-hidden"); }, 4500);
      pano.hidden = false;
      void pano.offsetWidth;
      pano.classList.add("is-open");
      pano.setAttribute("aria-hidden", "false");
      doc.body.style.overflow = "hidden";
      if (pImg.complete && pImg.naturalWidth) panoApply();
      else pImg.onload = panoApply;
      if (!ps.raf) ps.raf = requestAnimationFrame(panoLoop);
    }
    function closePano() {
      if (!pano) return;
      pano.classList.remove("is-open");
      pano.setAttribute("aria-hidden", "true");
      if (ps.raf) { cancelAnimationFrame(ps.raf); ps.raf = null; }
      window.setTimeout(function () {
        pano.hidden = true;
        if (modal.classList.contains("is-open")) startAuto();
      }, 350);
    }

    if (pano) {
      pStage.addEventListener("pointerdown", function (e) {
        ps.dragging = true; ps.drift = false; ps.lx = e.clientX; ps.ly = e.clientY;
        ps.vx = 0; ps.vy = 0; pStage.classList.add("is-grabbing");
        if (pHint) pHint.classList.add("is-hidden");
        if (pStage.setPointerCapture) { try { pStage.setPointerCapture(e.pointerId); } catch (err) {} }
      });
      pStage.addEventListener("pointermove", function (e) {
        if (!ps.dragging) return;
        var dx = e.clientX - ps.lx, dy = e.clientY - ps.ly;
        ps.lx = e.clientX; ps.ly = e.clientY;
        ps.x += dx; ps.y += dy; ps.vx = dx; ps.vy = dy;
        panoApply();
      });
      var endDrag = function () { ps.dragging = false; pStage.classList.remove("is-grabbing"); };
      pStage.addEventListener("pointerup", endDrag);
      pStage.addEventListener("pointercancel", endDrag);
      pStage.addEventListener("pointerleave", endDrag);
      pStage.addEventListener("wheel", function (e) {
        e.preventDefault(); panoZoom(e.deltaY < 0 ? 0.14 : -0.14);
      }, { passive: false });
      if (pZoomIn) pZoomIn.addEventListener("click", function () { panoZoom(0.25); });
      if (pZoomOut) pZoomOut.addEventListener("click", function () { panoZoom(-0.25); });
      pano.querySelectorAll("[data-pano-close]").forEach(function (c) {
        c.addEventListener("click", closePano);
      });
    }

    // Open the 360° view from a gallery cell or the caption button
    cells.forEach(function (c, i) {
      c.addEventListener("click", function () {
        if (i === current) openPano(i);
        else { goTo(i); resetAuto(); }
      });
    });
    var btn360 = modal.querySelector("[data-vsr-360]");
    if (btn360) btn360.addEventListener("click", function () { openPano(current); });

    doc.addEventListener("keydown", function (e) {
      if (pano && !pano.hidden) { if (e.key === "Escape") closePano(); return; }
      if (modal.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowRight") { next(); resetAuto(); }
      else if (e.key === "ArrowLeft") { prev(); resetAuto(); }
    });
    window.addEventListener("resize", function () {
      if (!modal.hidden) { computeRadius(); render(); }
      if (pano && !pano.hidden) panoApply();
    });
  })();

  /* ---- Reveal modals (Blog / Stay Lifted open from a card) ------------- */
  (function () {
    var openers = doc.querySelectorAll("[data-rmodal-open]");
    if (!openers.length) return;
    var current = null;

    function openModal(name) {
      var m = doc.querySelector('[data-rmodal="' + name + '"]');
      if (!m) return;
      current = m;
      m.hidden = false;
      void m.offsetWidth;
      m.classList.add("is-open");
      m.setAttribute("aria-hidden", "false");
      doc.body.style.overflow = "hidden";
    }
    function closeModal() {
      if (!current) return;
      var m = current;
      m.classList.remove("is-open");
      m.setAttribute("aria-hidden", "true");
      doc.body.style.overflow = "";
      window.setTimeout(function () { m.hidden = true; }, 350);
      current = null;
    }

    openers.forEach(function (o) {
      o.addEventListener("click", function () { openModal(o.getAttribute("data-rmodal-open")); });
    });
    doc.querySelectorAll("[data-rmodal-close]").forEach(function (c) {
      c.addEventListener("click", closeModal);
    });
    doc.addEventListener("keydown", function (e) {
      if (current && e.key === "Escape") closeModal();
    });
  })();

  /* ---- Count-up stat numbers -------------------------------------------- */
  function animateCount(el) {
    var raw = el.getAttribute("data-count") || el.textContent.trim();
    var match = raw.match(/^(\D*)(\d+)(.*)$/);
    if (!match) { el.textContent = raw; return; }
    var prefix = match[1], target = parseInt(match[2], 10), suffix = match[3];
    if (reduceMotion || target === 0) { el.textContent = prefix + target + suffix; return; }
    var start = null, dur = 1400;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  var counters = doc.querySelectorAll(".stat b, .hero__trust b");
  if ("IntersectionObserver" in window && counters.length) {
    counters.forEach(function (el) {
      if (!el.getAttribute("data-count")) el.setAttribute("data-count", el.textContent.trim());
    });
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          cio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---- Hero parallax (subtle) ------------------------------------------- */
  var heroBg = doc.querySelector(".hero__bg img");
  var hero = doc.querySelector(".hero");
  if (heroBg && hero && !reduceMotion) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        var h = hero.offsetHeight;
        if (y < h) {
          heroBg.style.transform = "translateY(" + (y * 0.06) + "px) scale(1.12)";
        }
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---- Smooth anchor scrolling ------------------------------------------ */
  doc.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (id.length < 2) return;
      var tgt = doc.querySelector(id);
      if (tgt) {
        e.preventDefault();
        tgt.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      }
    });
  });

  /* ---- Native lazy-loading for below-the-fold images -------------------- */
  doc.querySelectorAll("img").forEach(function (img) {
    if (img.closest(".hero, .nav")) return;      // keep above-the-fold eager
    if (!img.hasAttribute("loading")) img.setAttribute("loading", "lazy");
    img.setAttribute("decoding", "async");
  });

  /* ---- AI site assistant (chat widget) ---------------------------------- */
  (function () {
    var fab = doc.getElementById("chatFab");
    var panel = doc.getElementById("chatbot");
    var body = doc.getElementById("chatBody");
    var chips = doc.getElementById("chatChips");
    var form = doc.getElementById("chatForm");
    var input = doc.getElementById("chatInput");
    if (!fab || !panel || !body || !form || !input) return;

    var greeted = false;
    var busy = false;

    function scrollDown() { body.scrollTop = body.scrollHeight; }

    function addMsg(text, who) {
      var row = doc.createElement("div");
      row.className = "chat-msg chat-msg--" + who;
      var bubble = doc.createElement("div");
      bubble.className = "chat-bubble";
      // Preserve line breaks from the assistant, escape everything else.
      String(text).split("\n").forEach(function (line, i) {
        if (i) bubble.appendChild(doc.createElement("br"));
        bubble.appendChild(doc.createTextNode(line));
      });
      row.appendChild(bubble);
      body.appendChild(row);
      scrollDown();
      return bubble;
    }

    function addLinks(links) {
      if (!links || !links.length) return;
      var wrap = doc.createElement("div");
      wrap.className = "chat-links";
      links.forEach(function (l) {
        var a = doc.createElement("a");
        a.className = "chat-link";
        a.href = l.url;
        a.textContent = l.label;
        if (/^https?:/i.test(l.url)) { a.target = "_blank"; a.rel = "noopener"; }
        wrap.appendChild(a);
      });
      body.appendChild(wrap);
      scrollDown();
    }

    function renderChips(list) {
      chips.innerHTML = "";
      (list || []).forEach(function (label) {
        var b = doc.createElement("button");
        b.type = "button";
        b.className = "chat-chip";
        b.textContent = label;
        b.addEventListener("click", function () { send(label); });
        chips.appendChild(b);
      });
    }

    function typing(on) {
      var ex = doc.getElementById("chatTyping");
      if (on) {
        if (ex) return;
        var row = doc.createElement("div");
        row.className = "chat-msg chat-msg--bot";
        row.id = "chatTyping";
        row.innerHTML = '<div class="chat-bubble chat-typing"><span></span><span></span><span></span></div>';
        body.appendChild(row);
        scrollDown();
      } else if (ex) { ex.remove(); }
    }

    function send(text) {
      text = (text || "").trim();
      if (!text || busy) return;
      addMsg(text, "user");
      renderChips([]);
      input.value = "";
      busy = true;
      typing(true);
      fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      }).then(function (r) { return r.json(); }).then(function (data) {
        typing(false);
        addMsg(data.reply, "bot");
        addLinks(data.links);
        renderChips(data.chips);
        busy = false;
      }).catch(function () {
        typing(false);
        addMsg("Sorry, I couldn't reach the server. Please try again, or call us at " +
               "+91 85110 33826.", "bot");
        busy = false;
      });
    }

    function greet() {
      if (greeted) return;
      greeted = true;
      addMsg("Hi! 👋 I'm the Silex Assistant. Ask me about our elevators, pricing, " +
             "AMC plans or how to reach us.", "bot");
      renderChips(["Products", "Get a quote", "AMC & maintenance", "Contact"]);
    }

    function openChat() {
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      fab.setAttribute("aria-expanded", "true");
      doc.body.classList.add("chat-open");
      greet();
      window.setTimeout(function () { input.focus(); }, 250);
    }
    function closeChat() {
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      fab.setAttribute("aria-expanded", "false");
      doc.body.classList.remove("chat-open");
    }

    fab.addEventListener("click", function () {
      if (panel.classList.contains("is-open")) closeChat(); else openChat();
    });
    var closeBtn = doc.getElementById("chatClose");
    if (closeBtn) closeBtn.addEventListener("click", closeChat);
    form.addEventListener("submit", function (e) { e.preventDefault(); send(input.value); });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && panel.classList.contains("is-open")) closeChat();
    });
  })();

  /* ---- Image lightbox · tap any photo to view it full-size -------------- */
  (function () {
    // Chrome/UI images we never want to open in the viewer.
    var EXCLUDE = ".nav, .brand, .silex-splash, [data-lift-intro], .lift-intro," +
      " .chatbot, #chatFab, .chat-fab, .footer__brand, [data-vsr-modal]," +
      " [data-vsr-open], [data-carousel], [data-panels], .imgview, .hero__bg, .hero";

    function isPhoto(img) {
      if (!img || img.tagName !== "IMG") return false;
      if (img.closest(EXCLUDE)) return false;
      if (img.closest("a")) return false;            // keep linked images as links
      if (img.classList.contains("imgview__img")) return false;
      return true;
    }

    var overlay = null, viewImg = null;

    function build() {
      overlay = doc.createElement("div");
      overlay.className = "imgview";
      overlay.setAttribute("role", "dialog");
      overlay.setAttribute("aria-modal", "true");
      overlay.setAttribute("aria-hidden", "true");
      viewImg = doc.createElement("img");
      viewImg.className = "imgview__img";
      viewImg.alt = "";
      var close = doc.createElement("button");
      close.type = "button";
      close.className = "imgview__close";
      close.setAttribute("aria-label", "Close");
      close.innerHTML = "&times;";
      overlay.appendChild(viewImg);
      overlay.appendChild(close);
      doc.body.appendChild(overlay);
      overlay.addEventListener("click", closeView);
      close.addEventListener("click", closeView);
      // block the long-press "save image" menu inside the viewer
      overlay.addEventListener("contextmenu", function (e) { e.preventDefault(); });
    }

    function openView(src, alt) {
      if (!overlay) build();
      viewImg.src = src;
      viewImg.alt = alt || "";
      void overlay.offsetWidth;
      overlay.classList.add("is-open");
      overlay.setAttribute("aria-hidden", "false");
      doc.body.style.overflow = "hidden";
    }
    function closeView() {
      if (!overlay) return;
      overlay.classList.remove("is-open");
      overlay.setAttribute("aria-hidden", "true");
      doc.body.style.overflow = "";
    }

    doc.addEventListener("click", function (e) {
      var img = e.target.closest ? e.target.closest("img") : null;
      if (!img) {
        // photo may sit under a tile / figure overlay that swallows the click
        var host = e.target.closest && e.target.closest(".tile, figure, picture, .pcard__media");
        if (host && !host.closest("a")) img = host.querySelector("img");
      }
      if (!img || !isPhoto(img)) return;
      e.preventDefault();
      openView(img.currentSrc || img.src, img.alt);
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && overlay && overlay.classList.contains("is-open")) closeView();
    });

    // Flag qualifying photos so they show a zoom-in cursor.
    doc.querySelectorAll("img").forEach(function (img) {
      if (!isPhoto(img)) return;
      img.classList.add("zoomable");
      var host = img.closest(".tile, figure, picture, .pcard__media");
      if (host && !host.closest("a")) host.classList.add("zoomable");
    });
  })();

  /* ---- Luxury motion · cursor, magnetic, tilt, ripple, hero light ------ */
  (function () {
    var finePointer = window.matchMedia("(pointer: fine)").matches;
    var canMotion = finePointer && !reduceMotion;

    /* Hero mouse-light — follows the pointer inside the hero */
    var hero = doc.querySelector(".hero");
    if (hero && !reduceMotion) {
      if (!hero.querySelector(".hero__light")) {
        var light = doc.createElement("div");
        light.className = "hero__light";
        hero.appendChild(light);
      }
      hero.addEventListener("pointermove", function (e) {
        var r = hero.getBoundingClientRect();
        hero.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100) + "%");
        hero.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100) + "%");
      }, { passive: true });
    }

    /* Ripple on every button */
    doc.addEventListener("pointerdown", function (e) {
      var btn = e.target.closest && e.target.closest(".btn");
      if (!btn) return;
      var r = btn.getBoundingClientRect();
      var d = Math.max(r.width, r.height) * 2;
      var rip = doc.createElement("span");
      rip.className = "ripple";
      rip.style.width = rip.style.height = d + "px";
      rip.style.left = (e.clientX - r.left) + "px";
      rip.style.top = (e.clientY - r.top) + "px";
      btn.appendChild(rip);
      window.setTimeout(function () { rip.remove(); }, 600);
    });

    if (!canMotion) return;   // cursor / magnet / tilt are desktop-only polish

    /* Custom cursor — dot + trailing ring */
    var dot = doc.createElement("div"); dot.className = "cur-dot";
    var ring = doc.createElement("div"); ring.className = "cur-ring";
    doc.body.appendChild(dot); doc.body.appendChild(ring);
    doc.body.classList.add("has-cursor");
    var mx = window.innerWidth / 2, my = window.innerHeight / 2;
    var rx = mx, ry = my, started = false;
    window.addEventListener("pointermove", function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = "translate(" + mx + "px," + my + "px) translate(-50%,-50%)";
      if (!started) { started = true; doc.body.classList.add("cursor-ready"); }
    }, { passive: true });
    (function ringLoop() {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      ring.style.transform = "translate(" + rx + "px," + ry + "px) translate(-50%,-50%)";
      requestAnimationFrame(ringLoop);
    })();
    var HOVER = "a, button, .btn, input, textarea, select, [data-tilt], .pcard, .tile, summary";
    doc.addEventListener("pointerover", function (e) {
      if (e.target.closest && e.target.closest(HOVER)) doc.body.classList.add("cur-hover");
    });
    doc.addEventListener("pointerout", function (e) {
      if (e.target.closest && e.target.closest(HOVER)) doc.body.classList.remove("cur-hover");
    });
    window.addEventListener("pointerdown", function () { doc.body.classList.add("cur-down"); });
    window.addEventListener("pointerup", function () { doc.body.classList.remove("cur-down"); });
    doc.addEventListener("mouseleave", function () { doc.body.classList.remove("cursor-ready"); });
    doc.addEventListener("mouseenter", function () { doc.body.classList.add("cursor-ready"); });

    /* Magnetic buttons — gentle pull toward the pointer */
    doc.querySelectorAll(".btn--gold, .btn--navy, .nav__cta, [data-magnetic]").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2;
        var y = e.clientY - r.top - r.height / 2;
        el.style.transform = "translate(" + x * 0.25 + "px," + y * 0.35 + "px)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });

    /* 3D tilt on flagged cards */
    doc.querySelectorAll("[data-tilt]").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(900px) rotateY(" + (px * 8) + "deg) rotateX(" +
          (-py * 8) + "deg) translateZ(0)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
  })();
})();

