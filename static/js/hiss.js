// Tape Hiss Toggle
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    const hissToggle = document.getElementById('hissToggle');
    if (!hissToggle) return;

    // Create audio element for hiss
    const hiss = new Audio('/static/music/tape_hiss.mp3');
    hiss.loop = true;
    hiss.volume = 0.15;

    const saved = localStorage.getItem('hiss');
    if (saved === 'on') {
      hiss.play().catch(() => {});
      updateIcon(true);
    }

    hissToggle.addEventListener('click', function() {
      const isOn = hiss.paused;
      if (isOn) {
        hiss.play().catch(() => {});
      } else {
        hiss.pause();
      }
      localStorage.setItem('hiss', isOn ? 'on' : 'off');
      updateIcon(isOn);
    });

    function updateIcon(on) {
      const i = hissToggle.querySelector('i');
      i.className = on ? 'fas fa-volume-up' : 'fas fa-waveform';
    }
  });
})();