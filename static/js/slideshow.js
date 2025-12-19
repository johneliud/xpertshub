document.addEventListener('DOMContentLoaded', function() {
  const categories = [
    { name: 'Plumbing', image: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&h=400&fit=crop' },
    { name: 'Painting', image: 'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=600&h=400&fit=crop' },
    { name: 'Housekeeping', image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop' },
    { name: 'Electricity', image: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=600&h=400&fit=crop' },
    { name: 'Air Conditioner', image: 'https://images.unsplash.com/photo-1631545806609-c2b999c8f4c6?w=600&h=400&fit=crop' },
    { name: 'Carpentry', image: 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600&h=400&fit=crop' },
    { name: 'Gardening', image: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=400&fit=crop' },
    { name: 'Interior Design', image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop' }
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

  // Auto-advance every 4 seconds
  setInterval(nextSlide, 4000);
});
