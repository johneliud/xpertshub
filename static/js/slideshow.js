document.addEventListener('DOMContentLoaded', function() {
  const categories = [
    { name: 'Plumbing', image: 'static/images/slideshow/plumbing.jpg' },
    { name: 'Painting', image: 'static/images/slideshow/painting.jpg' },
    { name: 'Housekeeping', image: 'static/images/slideshow/housekeeping.jpg' },
    { name: 'Electricity', image: 'static/images/slideshow/electricity.jpg' },
    // { name: 'Air Conditioner', image: 'static/images/slideshow/air-conditioner.jpg' },
    { name: 'Carpentry', image: 'static/images/slideshow/carpentry.jpg' },
    { name: 'Gardening', image: 'static/images/slideshow/gardening.jpg' },
    { name: 'Interior Design', image: 'static/images/slideshow/interior-design.jpg' }
  ];

  const container = document.getElementById('slideshow-container');
  const dotsContainer = document.getElementById('slideshow-dots');
  
  if (!container || !dotsContainer) return;
  
  let currentSlide = 0;

  // Create slides
  categories.forEach((category, index) => {
    const slide = document.createElement('div');
    slide.className = `absolute inset-0 transition-opacity duration-1000 ${index === 0 ? 'opacity-100' : 'opacity-0'}`;
    slide.innerHTML = `
      <img src="${category.image}" alt="${category.name}" class="w-full h-full object-cover">
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
      <div class="absolute bottom-6 left-6">
        <h3 class="text-white text-2xl font-bold">${category.name}</h3>
        <p class="text-white/80">Professional ${category.name.toLowerCase()} services</p>
      </div>
    `;
    container.appendChild(slide);

    // Create dot
    const dot = document.createElement('button');
    dot.className = `w-3 h-3 rounded-full transition-all duration-300 ${index === 0 ? 'bg-white' : 'bg-white/50'}`;
    dot.addEventListener('click', () => goToSlide(index));
    dotsContainer.appendChild(dot);
  });

  function goToSlide(index) {
    const slides = container.children;
    const dots = dotsContainer.children;
    
    slides[currentSlide].classList.remove('opacity-100');
    slides[currentSlide].classList.add('opacity-0');
    dots[currentSlide].classList.remove('bg-white');
    dots[currentSlide].classList.add('bg-white/50');
    
    currentSlide = index;
    
    slides[currentSlide].classList.remove('opacity-0');
    slides[currentSlide].classList.add('opacity-100');
    dots[currentSlide].classList.remove('bg-white/50');
    dots[currentSlide].classList.add('bg-white');
  }

  function nextSlide() {
    const nextIndex = (currentSlide + 1) % categories.length;
    goToSlide(nextIndex);
  }

  // Auto-advance every 5 seconds
  setInterval(nextSlide, 5000);
});
