const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('visible');
            observer.unobserve(e.target);
        }
    });
}, { threshold: 0.12 });

document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));

function animateCount(el, target) {
    let current = 0;
    const step = target / 60;
    const timer = setInterval(() => {
        current += step;
        if (current >= target) { el.textContent = target + (target === 98 ? '%' : '+'); clearInterval(timer); }
        else el.textContent = Math.floor(current) + (target === 98 ? '%' : '+');
    }, 24);
}

const countObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.querySelectorAll('[data-count]').forEach(num => {
                animateCount(num, +num.dataset.count);
            });
            countObs.unobserve(e.target);
        }
    });
}, { threshold: 0.3 });

document.querySelectorAll('.stats-bar').forEach(el => countObs.observe(el));