/* =============================================
   sB LIVE COUNTDOWN - JAVASCRIPT
   ============================================= */

// =============================================
// TARGET DATES
// =============================================
const WEDDING_DATE = new Date('2026-03-26T17:00:00+02:00');
const USA_DATE = new Date('2026-06-07T00:00:00+02:00');
const DOLOMITES_DATE = new Date('2026-05-04T00:00:00+02:00');

// =============================================
// COUNTDOWN LOGIC
// =============================================
function updateCountdown(targetDate, elements) {
    const now = new Date();
    const diff = targetDate - now;

    if (diff <= 0) {
        Object.values(elements).forEach(el => {
            if (el) el.textContent = '🎉';
        });
        return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    if (elements.days) elements.days.textContent = String(days).padStart(2, '0');
    if (elements.hours) elements.hours.textContent = String(hours).padStart(2, '0');
    if (elements.minutes) elements.minutes.textContent = String(minutes).padStart(2, '0');
    if (elements.seconds) elements.seconds.textContent = String(seconds).padStart(2, '0');
}

function startCountdowns() {
    // Wedding countdown
    const weddingEls = {
        days: document.getElementById('wDays'),
        hours: document.getElementById('wHours'),
        minutes: document.getElementById('wMinutes'),
        seconds: document.getElementById('wSeconds')
    };

    // USA Honeymoon countdown
    const usaEls = {
        days: document.getElementById('uDays'),
        hours: document.getElementById('uHours'),
        minutes: document.getElementById('uMinutes')
    };

    // Dolomites countdown
    const dolomitesEls = {
        days: document.getElementById('dDays'),
        hours: document.getElementById('dHours'),
        minutes: document.getElementById('dMinutes')
    };

    // Update immediately
    updateCountdown(WEDDING_DATE, weddingEls);
    updateCountdown(USA_DATE, usaEls);
    updateCountdown(DOLOMITES_DATE, dolomitesEls);

    // Update every second
    setInterval(() => {
        updateCountdown(WEDDING_DATE, weddingEls);
        updateCountdown(USA_DATE, usaEls);
        updateCountdown(DOLOMITES_DATE, dolomitesEls);
    }, 1000);
}

// =============================================
// PARTICLES BACKGROUND
// =============================================
function createParticles() {
    const container = document.getElementById('particles');
    const count = window.innerWidth < 768 ? 30 : 60;

    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.width = (Math.random() * 3 + 1) + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
        particle.style.animationDelay = Math.random() * 10 + 's';
        particle.style.opacity = Math.random() * 0.5 + 0.1;

        // Random colors: gold, pink, white
        const colors = [
            'rgba(255, 215, 0, 0.4)',
            'rgba(255, 107, 157, 0.3)',
            'rgba(255, 255, 255, 0.2)'
        ];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];

        container.appendChild(particle);
    }
}

// =============================================
// FLOATING HEARTS
// =============================================
function createFloatingHearts() {
    const hearts = ['💕', '💖', '💗', '❤️', '💘', '🤍'];
    const container = document.getElementById('particles');

    function spawnHeart() {
        const heart = document.createElement('span');
        heart.classList.add('floating-heart');
        heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
        heart.style.left = Math.random() * 100 + '%';
        heart.style.fontSize = (Math.random() * 14 + 8) + 'px';
        heart.style.animationDuration = (Math.random() * 6 + 6) + 's';
        heart.style.opacity = Math.random() * 0.4 + 0.1;
        container.appendChild(heart);

        heart.addEventListener('animationend', () => heart.remove());
    }

    // Spawn a heart every 800ms
    setInterval(spawnHeart, 800);
}
// SCROLL REVEAL
// =============================================
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.trip-card').forEach(card => {
        observer.observe(card);
    });
}

// =============================================
// IMAGE CACHE BUST
// =============================================
function bustImageCache() {
    // Add timestamp to image URLs to bypass cache and show latest AI-generated image
    const today = new Date().toISOString().split('T')[0];
    const usaImg = document.getElementById('usaImage');
    const dolImg = document.getElementById('dolomitesImage');

    if (usaImg) usaImg.src = `images/usa-honeymoon.png?v=${today}`;
    if (dolImg) dolImg.src = `images/dolomites-minimoon.png?v=${today}`;
}

// =============================================
// INIT
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    createFloatingHearts();
    startCountdowns();
    initScrollReveal();
    bustImageCache();
});
