// script.js
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('navToggle');
    const menu = document.getElementById('navbarMenu');

    if (toggleBtn && menu) {
        toggleBtn.addEventListener('click', () => {
            toggleBtn.classList.toggle('active');
            menu.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && !toggleBtn.contains(e.target)) {
                toggleBtn.classList.remove('active');
                menu.classList.remove('show');
            }
        });
    }
});
