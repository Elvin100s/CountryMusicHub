// Vintage Mode management
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    const vintageToggle = document.getElementById('vintageToggle');
    const html = document.documentElement;

    if (!vintageToggle) return;

    // Load saved preference
    const savedVintage = localStorage.getItem('vintage');
    if (savedVintage === 'on') {
      html.classList.add('vintage-mode');
      updateIcon(true);
    }

    vintageToggle.addEventListener('click', function() {
      const isOn = html.classList.toggle('vintage-mode');
      localStorage.setItem('vintage', isOn ? 'on' : 'off');
      updateIcon(isOn);
    });

    function updateIcon(isOn) {
      const icon = vintageToggle.querySelector('i');
      icon.className = isOn ? 'fas fa-music' : 'fas fa-record-vinyl';
    }
  });
})();