/* ==================================================
   Soft Minimalism / Soft-Morphism – Universal JS
   Handles UI effects, animations, events, data, themes
=================================================== */
(() => {
  "use strict";

  /* ===================================================
     1. Theme Switcher
  ==================================================== */
  const ThemeManager = {
    currentTheme: "light",
    availableThemes: ["light", "dark", "high-contrast", "soft-alt"],

    setTheme(theme) {
  // Ignore invalid themes to prevent applying unsupported or unsafe values
  if (!this.availableThemes.includes(theme)) return;
  document.documentElement.setAttribute("data-theme", theme);
  // Add/remove .dark class for Tailwind compatibility
  if (theme === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
  this.currentTheme = theme;
},

    toggleTheme() {
      let index = this.availableThemes.indexOf(this.currentTheme);
      index = (index + 1) % this.availableThemes.length;
      this.setTheme(this.availableThemes[index]);
    }
  };

  /* ===================================================
     2. Utilities
  ==================================================== */
  const selectAll = (selector, parent = document) => Array.from(parent.querySelectorAll(selector));
  const selectOne = (selector, parent = document) => parent.querySelector(selector);
  const $ = (selector, parent = document) => parent.querySelector(selector);

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  const debounce = (fn, delay = 100) => {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
    };
  };

  /* ===================================================
     3. Buttons & CTA effects
  ==================================================== */
  function initButtons() {
    selectAll("button, .btn").forEach(btn => {
      btn.addEventListener("click", e => {
        if (btn.disabled) return;
        btn.classList.add("active");
        setTimeout(() => btn.classList.remove("active"), 150);
      });
    });
  }

  /* ===================================================
     4. Tabs
  ==================================================== */
  function initTabs() {
    selectAll(".tabs").forEach(tabGroup => {
      const tabs = selectAll(".tab", tabGroup);
      tabs.forEach(tab => {
        tab.addEventListener("click", () => {
          tabs.forEach(t => t.classList.remove("active"));
          tab.classList.add("active");
          const target = tab.dataset.target;
          if (target) {
            selectAll(`${target}`).forEach(el => el.style.display = "block");
            tabs.filter(t => t.dataset.target !== target)
              .forEach(t => {
                if (t.dataset.target) selectAll(`${t.dataset.target}`).forEach(el => el.style.display = "none");
              });
          }
        });
      });
    });
  }

  /* ===================================================
     5. Accordion
  ==================================================== */
  function initAccordions() {
    selectAll(".accordion-header").forEach(header => {
      header.addEventListener("click", () => {
        const item = header.parentElement;
        item.classList.toggle("active");
      });
    });
  }

  /* ===================================================
     6. Modal
  ==================================================== */
  function initModals() {
    selectAll("[data-modal-target]").forEach(trigger => {
      const modalId = trigger.dataset.modalTarget;
      const modal = selectOne(`#${modalId}`);
      if (!modal) return;
      let overlay = $(".modal-overlay", modal.parentElement);
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "modal-overlay";
        document.body.appendChild(overlay);
      }
      const closeButtons = selectAll(".modal-close", modal);
      const openModal = () => {
        modal.style.display = "block";
        overlay.style.display = "flex";
        setTimeout(() => modal.classList.add("fade-in"), 20);
      };
      const closeModal = () => {
        modal.classList.remove("fade-in");
        modal.style.display = "none";
        overlay.style.display = "none";
      };
      trigger.addEventListener("click", openModal);
      overlay.addEventListener("click", closeModal);
      closeButtons.forEach(btn => btn.addEventListener("click", closeModal));
    });
  }

  /* ===================================================
     7. Tooltips
  ==================================================== */
  function initTooltips() {
    selectAll(".tooltip").forEach(tt => {
      const tip = selectOne(".tooltiptext", tt);
      if (!tip) return;
      tt.addEventListener("mouseenter", () => tip.style.visibility = "visible");
      tt.addEventListener("mouseleave", () => tip.style.visibility = "hidden");
    });
  }

  /* ===================================================
     8. Progress bars
  ==================================================== */
  const setProgress = (selector, value) => {
    selectAll(`${selector}`).forEach(bar => {
      const fill = selectOne(".progress-bar-fill", bar);
      if (fill) fill.style.width = `${clamp(value, 0, 100)}%`;
    });
  };

  /* ===================================================
     9. Dynamic data loading
  ==================================================== */
  const loadData = (selector, data) => {
    selectAll(`${selector}`).forEach(el => {
      if (Array.isArray(data)) el.innerHTML = data.join("");
      else if (typeof data === "string") el.innerHTML = data;
    });
  };

  /* ===================================================
     10. Animations & movement helpers
  ==================================================== */
  const animateCSS = (element, animationName, callback) => {
    element.classList.add(animationName);
    const handleAnimationEnd = () => {
      element.classList.remove(animationName);
      element.removeEventListener("animationend", handleAnimationEnd);
      if (typeof callback === "function") callback();
    };
    element.addEventListener("animationend", handleAnimationEnd);
  };

  /* ===================================================
     11. Initialize all components
  ==================================================== */
  const initUI = () => {
    initButtons();
    initTabs();
    initAccordions();
    initModals();
    initTooltips();
  };

  /* ===================================================
     12. Document ready
  ==================================================== */
  document.addEventListener("DOMContentLoaded", initUI);

  /* ===================================================
     13. Expose global utilities
  ==================================================== */
  window.UI = {
    ThemeManager,
    setProgress,
    loadData,
    animateCSS
  };
})();

// Parallax background effect
const parallaxBg = document.querySelector('.parallax-bg');
if (parallaxBg) {
  let mouseX = 0, mouseY = 0;
  let posX = 0, posY = 0;

  const draw = () => {
    posX += (mouseX - posX) * 0.05;
    posY += (mouseY - posY) * 0.05;
    parallaxBg.style.transform = `translate(${posX / 20}px, ${posY / 20}px) scale(1.2)`;
  window.addEventListener('mousemove', e => {
    const rect = parallaxBg.getBoundingClientRect();
    mouseX = e.clientX - rect.left - rect.width / 2;
    mouseY = e.clientY - rect.top - rect.height / 2;
  });
    mouseY = e.clientY - rect.top - rect.height / 2;
  };
  requestAnimationFrame(draw);
} else {
  console.warn("Parallax background element not found.");
}

// Example: Using debounce to limit how often the resize event handler runs, improving performance on window resize
const resizeHandler = debounce(() => {
  console.log("Window resized");
}, 200);
window.addEventListener('resize', resizeHandler);   
// </script> --- IGNORE ---
/* ==================================================
   Soft Minimalism / Soft-Morphism – Universal JS
   Handles UI effects, animations, events, data, themes
=================================================== */

