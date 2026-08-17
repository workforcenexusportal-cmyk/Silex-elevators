/* =========================================================================
   SILEX ELEVATOR — front-end interactions
   Smooth, silent, smart micro-interactions (logolift-inspired)
   ========================================================================= */
(function () {
  "use strict";

  var doc = document;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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
  if (toggle && links) {
    function setMenu(open) {
      links.classList.toggle("open", open);
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

    window.addEventListener("resize", function () {
      if (window.innerWidth > 980) setMenu(false);
    });

    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  /* ---- Nav dropdown accordions (mobile) --------------------------------- */
  doc.querySelectorAll(".drop-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var parent = btn.closest(".has-drop");
      if (!parent) return;
      var isOpen = parent.classList.contains("open");
      // Close siblings for a clean accordion feel.
      doc.querySelectorAll(".has-drop.open").forEach(function (o) {
        if (o !== parent) o.classList.remove("open");
      });
      parent.classList.toggle("open", !isOpen);
    });
  });

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
})();
