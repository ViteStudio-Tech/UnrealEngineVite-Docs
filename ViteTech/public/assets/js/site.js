/* Vite Technology — progressive enhancement only. Every page reads and
   navigates correctly with this file blocked. */
(() => {
    document.documentElement.classList.add("js");

    // Mobile navigation.
    const toggle = document.querySelector(".nav__toggle");
    const nav = document.getElementById("site-nav");
    if (toggle && nav) {
        toggle.addEventListener("click", () => {
            const open = nav.classList.toggle("is-open");
            toggle.setAttribute("aria-expanded", String(open));
        });
        nav.addEventListener("click", (event) => {
            if (event.target.closest("a")) {
                nav.classList.remove("is-open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });
    }

    // Fade sections in once. Skipped entirely when motion is reduced or
    // IntersectionObserver is missing, so nothing is ever left hidden.
    const reveals = document.querySelectorAll(".reveal");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reduce && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            for (const entry of entries) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            }
        }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
        reveals.forEach((el) => observer.observe(el));
    } else {
        reveals.forEach((el) => el.classList.add("is-visible"));
    }

    const year = document.querySelector("[data-year]");
    if (year) {
        year.textContent = String(new Date().getFullYear());
    }
})();
