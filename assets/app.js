/* ==========================================================================
   RACHIT PANDEY — interaction layer
   Zero dependencies. Everything degrades gracefully without JS.
   ========================================================================== */
(() => {
  "use strict";
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- 1. Rotating role headline ---------------------------------------- */
  const roleHost = $("[data-role-swap]");
  if (roleHost) {
    const roles = (roleHost.dataset.roles || "").split("|").map((r) => r.trim()).filter(Boolean);
    if (roles.length && !reduced) {
      const nodes = roles.map((r) => {
        const el = document.createElement("span");
        el.textContent = r;
        roleHost.appendChild(el);
        return el;
      });
      let i = 0;
      nodes[0].classList.add("on");
      setInterval(() => {
        nodes[i].classList.remove("on");
        i = (i + 1) % nodes.length;
        nodes[i].classList.add("on");
      }, 2800);
    } else if (roles.length) {
      roleHost.textContent = roles[0];
    }
  }

  /* ---- 2. Terminal typing ----------------------------------------------- */
  const term = $("[data-terminal]");
  if (term && !reduced) {
    const reduce = $("[data-terminal-static]", term);
    const src = (term.dataset.script || "").split("\n").filter(Boolean);
    const esc = (t) =>
      t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
       .replace(/(fn|const|let|return|await|async|new|export|import)\b/g, '<span class="t-key">$1</span>')
       .replace(/(&quot;[^&]*?&quot;|'[^']*?'|"[^"]*?")/g, '<span class="t-str">$1</span>')
       .replace(/\b(\d+)\b/g, '<span class="t-num">$1</span>')
       .replace(/^(\$ )/g, '<span class="t-fn">$1</span>');

    const write = async (line, el) => {
      const parts = esc(line);
      // keep tags intact while revealing characters
      const tokens = parts.split(/(<span[^>]*>|<\/span>)/);
      for (const tk of tokens) {
        if (tk.startsWith("<span") || tk === "</span>") { el.insertAdjacentHTML("beforeend", tk); continue; }
        for (const ch of tk) {
          el.insertAdjacentText("beforeend", ch);
          if (Math.random() > 0.86) await sleep(16 + Math.random() * 34);
        }
      }
    };

    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

    (async () => {
      await sleep(420);
      for (const line of src) {
        const row = document.createElement("div");
        term.appendChild(row);
        await write(line, row);
        await sleep(190);
      }
      const c = document.createElement("span");
      c.className = "caret";
      term.appendChild(c);
      if (reduce) reduce.remove();
    })();
  }

  /* ---- 3. Scroll reveal --------------------------------------------------- */
  const reveals = $$(".reveal");
  if (reveals.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      reveals.forEach((el) => el.classList.add("in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const d = +(e.target.dataset.delay || 0);
          setTimeout(() => e.target.classList.add("in"), d);
          io.unobserve(e.target);
        }),
        { threshold: 0.12, rootMargin: "0px 0px -40px" }
      );
      reveals.forEach((el) => io.observe(el));
    }
  }

  /* ---- 4. Animated stat counters ------------------------------------------ */
  const counters = $$("[data-count]");
  const runCount = (el) => {
    const target = parseFloat(el.dataset.count);
    const dur = 1400;
    const t0 = performance.now();
    const step = (t) => {
      const p = Math.min((t - t0) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      const v = target * eased;
      el.textContent = Number.isInteger(target) ? Math.round(v).toString() : v.toFixed(1);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = el.dataset.suffix || target;
    };
    requestAnimationFrame(step);
  };
  if (counters.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      counters.forEach((el) => (el.textContent = (el.dataset.suffix || el.dataset.count)));
    } else {
      const io2 = new IntersectionObserver((entries) => entries.forEach((e) => {
        if (e.isIntersecting) { runCount(e.target); io2.unobserve(e.target); }
      }), { threshold: 0.5 });
      counters.forEach((el) => io2.observe(el));
    }
  }

  /* ---- 5. Skill bars fill on enter ----------------------------------------- */
  const bars = $$("[data-level]");
  const fill = (el) => { el.style.width = `${Math.min(+el.dataset.level, 100)}%`; };
  if (bars.length) {
    if (reduced || !("IntersectionObserver" in window)) bars.forEach(fill);
    else {
      const io3 = new IntersectionObserver((entries) => entries.forEach((e) => {
        if (e.isIntersecting) { fill(e.target); io3.unobserve(e.target); }
      }), { threshold: 0.4 });
      bars.forEach((el) => io3.observe(el));
    }
  }

  /* ---- 6. Cursor spotlight on cards ---------------------------------------- */
  if (!reduced && window.matchMedia("(hover: hover)").matches) {
    $$(".card--spot").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", `${e.clientX - r.left}px`);
        card.style.setProperty("--my", `${e.clientY - r.top}px`);
      });
    });
  }

  /* ---- 7. Sticky navbar state ---------------------------------------------- */
  const nav = $(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("is-stuck", window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- 8. Marquee: duplicate track for seamless loop ------------------------- */
  $$(".marquee__track").forEach((track) => {
    track.append(...[...track.children].map((n) => n.cloneNode(true)));
  });

  /* ---- 9. Local time in footer ---------------------------------------------- */
  const clock = $("[data-clock]");
  if (clock) {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const paint = () => {
      const t = new Date().toLocaleTimeString("en-GB", {
        hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: tz,
      });
      clock.textContent = `${t} · ${tz.split("/").pop().replace(/_/g, " ")}`;
    };
    paint();
    setInterval(paint, 1000);
  }

  /* ---- 10. Year ---------------------------------------------------------------- */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();