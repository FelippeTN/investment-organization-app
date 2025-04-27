document.addEventListener('DOMContentLoaded', () => {
    console.log('sidebar.js loaded');
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('toggle-sidebar');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');

    if (sidebar && toggleButton && menuIcon && closeIcon) {
        console.log('Elements found, setting up toggle');
        toggleButton.addEventListener('click', () => {
            console.log('Toggle button clicked, current sidebar class:', sidebar.className);
            sidebar.classList.toggle('is-hidden');
            menuIcon.classList.toggle('hidden');
            closeIcon.classList.toggle('hidden');
            // On mobile, manage the 'hidden' class
            if (!sidebar.classList.contains('is-hidden')) {
                sidebar.classList.remove('hidden');
                console.log('Sidebar shown, removed hidden class');
            } else {
                console.log('Sidebar hidden, kept hidden class');
            }
            console.log('New sidebar class:', sidebar.className);
        });
    } else {
        console.log('One or more elements not found:', { sidebar, toggleButton, menuIcon, closeIcon });
    }
});