let dropdownOpen = false;

function toggleDropdown() {
  const menu = document.getElementById('dropdownMenu');
  const icon = document.getElementById('dropdownIcon');
  
  dropdownOpen = !dropdownOpen;
  
  if (dropdownOpen) {
    menu.classList.remove('hidden');
    icon.style.transform = 'rotate(180deg)';
  } else {
    menu.classList.add('hidden');
    icon.style.transform = 'rotate(0deg)';
  }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
  const dropdown = document.getElementById('servicesDropdown');
  if (!dropdown.contains(event.target) && dropdownOpen) {
    toggleDropdown();
  }
});

// Keep dropdown open when hovering over menu
document.addEventListener('DOMContentLoaded', function() {
  const dropdownMenu = document.getElementById('dropdownMenu');
  if (dropdownMenu) {
    dropdownMenu.addEventListener('mouseenter', function() {
      if (!dropdownOpen) {
        toggleDropdown();
      }
    });
  }
});
