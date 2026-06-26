/* ==========================================
   GitHub Insight AI - Elite Script (Part 1)
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    initializeTheme();

    initializeForm();

    initializeCounters();

    initializeAnimations();

    initializeScrollEffects();

});

/* ==========================================
   DARK / LIGHT MODE
========================================== */

function toggleTheme() {

    document.body.classList.toggle("light");

    const theme = document.body.classList.contains("light")
        ? "light"
        : "dark";

    localStorage.setItem("theme", theme);

}

function initializeTheme() {

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {

        document.body.classList.add("light");

    }

}

/* ==========================================
   FORM
========================================== */

function initializeForm() {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function () {

        showLoading();

    });

}

/* ==========================================
   LOADING BUTTON
========================================== */

function showLoading() {

    const button = document.querySelector("button[type='submit']");

    if (!button) return;

    button.disabled = true;

    button.innerHTML =

        `<span class="spinner-border spinner-border-sm"></span>
         Analyzing...`;

}

/* ==========================================
   COUNTER ANIMATION
========================================== */

function initializeCounters() {

    const counters = document.querySelectorAll(".stat-card h2");

    counters.forEach(counter => {

        const target = Number(counter.innerText);

        if (isNaN(target)) return;

        let value = 0;

        const increment = Math.max(1, Math.ceil(target / 100));

        const timer = setInterval(() => {

            value += increment;

            if (value >= target) {

                counter.innerText = target;

                clearInterval(timer);

            } else {

                counter.innerText = value;

            }

        }, 15);

    });

}

/* ==========================================
   FADE ANIMATION
========================================== */

function initializeAnimations() {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";

        card.style.transform = "translateY(40px)";

        setTimeout(() => {

            card.style.transition = ".6s";

            card.style.opacity = "1";

            card.style.transform = "translateY(0)";

        }, index * 120);

    });

}

/* ==========================================
   SMOOTH SCROLL
========================================== */

function initializeScrollEffects() {

    document.querySelectorAll("a[href^='#']").forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });

}

/* ==========================================
   COPY TO CLIPBOARD
========================================== */

function copyRepository(url) {

    navigator.clipboard.writeText(url);

    showToast("Repository URL copied!");

}

/* ==========================================
   TOAST
========================================== */

function showToast(message) {

    const toast = document.createElement("div");

    toast.className = "toast-message";

    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}

/* ==========================================
   EXPORT JSON
========================================== */

function exportJSON(data) {

    const blob = new Blob(

        [JSON.stringify(data, null, 4)],

        { type: "application/json" }

    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "repository-report.json";

    a.click();

}

/* ==========================================
   SCROLL TO TOP
========================================== */

function scrollTopPage() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}
/* ==========================================
   SEARCH HISTORY (LocalStorage)
========================================== */

function saveSearch(repoUrl) {

    let history = JSON.parse(localStorage.getItem("searchHistory")) || [];

    if (!history.includes(repoUrl)) {

        history.unshift(repoUrl);

    }

    history = history.slice(0, 10);

    localStorage.setItem
  /* ==========================================
   GitHub Insight AI - Elite Script (Part 3)
========================================== */

/* ---------- FAVORITES ---------- */

function toggleFavorite(repoName) {

    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];

    if (favorites.includes(repoName)) {

        favorites = favorites.filter(item => item !== repoName);

        showToast("Removed from Favorites ❤️");

    } else {

        favorites.push(repoName);

        showToast("Added to Favorites ⭐");

    }

    localStorage.setItem("favorites", JSON.stringify(favorites));

}

/* ---------- SEARCH VALIDATION ---------- */

function validateRepository(url) {

    const pattern = /^https:\/\/github\.com\/[^\/]+\/[^\/]+\/?$/;

    return pattern.test(url);

}

/* ---------- INPUT VALIDATION ---------- */

const repoInput = document.querySelector("input[name='repo_url']");

if (repoInput) {

    repoInput.addEventListener("blur", function () {

        if (this.value && !validateRepository(this.value)) {

            this.classList.add("is-invalid");

            showToast("Enter a valid GitHub repository URL.");

        } else {

            this.classList.remove("is-invalid");

        }

    });

}

/* ---------- SCORE ANIMATION ---------- */

function animateScore() {

    const score = document.querySelector(".score-circle h1");

    if (!score) return;

    const target = parseInt(score.innerText);

    if (isNaN(target)) return;

    let current = 0;

    const timer = setInterval(() => {

        current++;

        score.innerText = current;

        if (current >= target) {

            clearInterval(timer);

        }

    }, 15);

}

animateScore();

/* ---------- IMAGE HOVER ---------- */

document.querySelectorAll(".contributor-card img").forEach(img => {

    img.addEventListener("mouseenter", () => {

        img.style.transform = "scale(1.1) rotate(5deg)";

    });

    img.addEventListener("mouseleave", () => {

        img.style.transform = "scale(1) rotate(0deg)";

    });

});

/* ---------- BACK TO TOP BUTTON ---------- */

const topButton = document.createElement("button");

topButton.innerHTML = "⬆";

topButton.id = "topButton";

topButton.style.position = "fixed";
topButton.style.bottom = "20px";
topButton.style.right = "20px";
topButton.style.padding = "12px 18px";
topButton.style.border = "none";
topButton.style.borderRadius = "50%";
topButton.style.background = "#2563eb";
topButton.style.color = "#fff";
topButton.style.cursor = "pointer";
topButton.style.display = "none";
topButton.style.zIndex = "999";

document.body.appendChild(topButton);

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {

        topButton.style.display = "block";

    } else {

        topButton.style.display = "none";

    }

});

topButton.addEventListener("click", scrollTopPage);

/* ---------- KEYBOARD SHORTCUT ---------- */

document.addEventListener("keydown", function(e){

    if(e.key === "/"){

        e.preventDefault();

        if(repoInput){

            repoInput.focus();

        }

    }

});

/* ---------- SIMPLE LOADER ---------- */

window.addEventListener("load",()=>{

    document.body.classList.add("fade-in");

});

/* ---------- COPYRIGHT ---------- */

console.log("%cGitHub Insight AI","font-size:22px;color:#2563eb;font-weight:bold;");
console.log("Developed with Flask + GitHub API + Chart.js");
