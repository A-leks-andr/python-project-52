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

// Управление сообщениями

// static/js/main.js

document.addEventListener('DOMContentLoaded', (event) => {
    // Находим все наши кастомные кнопки закрытия
    const closeButtons = document.querySelectorAll('.my-close-btn');

    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // При клике получаем родительский элемент (.my-alert)
            const alertBox = this.parentElement;
            
            // Запускаем анимацию исчезновения (CSS transition)
            alertBox.style.opacity = '0';
            
            // Удаляем элемент из DOM после завершения анимации
            setTimeout(() => {
                alertBox.style.display = 'none';
                // Или alertBox.remove();
            }, 500); // 500ms должно совпадать с transition в CSS
        });
    });
});