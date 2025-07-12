// Testimonials Slider
let currentTestimonial = 0;
const testimonials = document.querySelectorAll(".testimonial");
const dots = document.querySelectorAll(".dot");

function showTestimonial(index) {
  testimonials.forEach((testimonial, i) => {
    testimonial.classList.toggle("active", i === index);
  });

  dots.forEach((dot, i) => {
    dot.classList.toggle("active", i === index);
  });

  currentTestimonial = index;
}

// Auto-slide testimonials
setInterval(() => {
  const nextIndex = (currentTestimonial + 1) % testimonials.length;
  showTestimonial(nextIndex);
}, 5000);

// Intersection Observer for fade-in animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -100px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "0";
      entry.target.style.transform = "translateY(30px)";

      setTimeout(() => {
        entry.target.style.transition = "all 0.6s ease";
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }, 100);

      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe elements
document.addEventListener("DOMContentLoaded", () => {
  const animatedElements = document.querySelectorAll(
    ".feature-card, .step, .section-title"
  );
  animatedElements.forEach((el) => observer.observe(el));
});

// Parallax Effect
window.addEventListener("scroll", () => {
  const scrolled = window.pageYOffset;
  const parallax = document.querySelector(".video-background");

  if (parallax) {
    parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
  }
});

// Mouse move effect for hero section
document.addEventListener("mousemove", (e) => {
  const hero = document.querySelector(".hero-content");
  if (!hero) return;

  const mouseX = e.clientX / window.innerWidth;
  const mouseY = e.clientY / window.innerHeight;

  const translateX = (mouseX - 0.5) * 20;
  const translateY = (mouseY - 0.5) * 20;

  hero.style.transform = `translate(${translateX}px, ${translateY}px)`;
});

// Add ripple effect to buttons
document.querySelectorAll("button").forEach((button) => {
  button.addEventListener("click", function (e) {
    const ripple = document.createElement("span");
    ripple.classList.add("ripple");

    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;

    // Add ripple styles
    const style = document.createElement("style");
    style.textContent = `
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                transform: scale(0);
                animation: ripple-animation 0.6s ease-out;
                pointer-events: none;
            }
            
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
    if (!document.querySelector("style[data-ripple]")) {
      style.setAttribute("data-ripple", "true");
      document.head.appendChild(style);
    }

    this.style.position = "relative";
    this.style.overflow = "hidden";
    this.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  });
});

// Loading animation for sections
function createLoadingAnimation() {
  const loadingHTML = `
        <div class="loading-container">
            <div class="loading-spinner">
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
            </div>
        </div>
    `;

  const style = document.createElement("style");
  style.textContent = `
        .loading-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 25, 47, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        
        .loading-spinner {
            position: relative;
            width: 80px;
            height: 80px;
        }
        
        .spinner-ring {
            position: absolute;
            width: 100%;
            height: 100%;
            border: 3px solid transparent;
            border-top-color: var(--cyan-glow);
            border-radius: 50%;
            animation: spin 1.5s linear infinite;
        }
        
        .spinner-ring:nth-child(2) {
            width: 70%;
            height: 70%;
            top: 15%;
            left: 15%;
            animation-delay: -0.5s;
        }
        
        .spinner-ring:nth-child(3) {
            width: 40%;
            height: 40%;
            top: 30%;
            left: 30%;
            animation-delay: -1s;
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
    `;

  document.head.appendChild(style);

  const container = document.createElement("div");
  container.innerHTML = loadingHTML;

  return container.firstElementChild;
}

// Counter animation for statistics
function animateCounter(element, target, duration = 2000) {
  const start = 0;
  const increment = target / (duration / 16);
  let current = start;

  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    element.textContent = Math.floor(current);
  }, 16);
}

// Smooth reveal animation for elements
function revealOnScroll() {
  const reveals = document.querySelectorAll(".reveal");

  reveals.forEach((reveal) => {
    const windowHeight = window.innerHeight;
    const elementTop = reveal.getBoundingClientRect().top;
    const elementVisible = 150;

    if (elementTop < windowHeight - elementVisible) {
      reveal.classList.add("active");
    }
  });
}

window.addEventListener("scroll", revealOnScroll);

// Typewriter effect
function typeWriter(element, text, speed = 50) {
  let i = 0;
  element.textContent = "";

  function type() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }

  type();
}

// Glitch effect for text
function addGlitchEffect(element) {
  element.classList.add("glitch");
  element.setAttribute("data-text", element.textContent);

  const style = document.createElement("style");
  style.textContent = `
        .glitch {
            position: relative;
            animation: glitch 2s infinite;
        }
        
        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .glitch::before {
            animation: glitch-1 0.5s infinite;
            color: var(--cyan-glow);
            z-index: -1;
        }
        
        .glitch::after {
            animation: glitch-2 0.5s infinite;
            color: #ff0080;
            z-index: -2;
        }
        
        @keyframes glitch {
            0%, 100% {
                transform: translate(0);
            }
            20% {
                transform: translate(-2px, 2px);
            }
            40% {
                transform: translate(-2px, -2px);
            }
            60% {
                transform: translate(2px, 2px);
            }
            80% {
                transform: translate(2px, -2px);
            }
        }
        
        @keyframes glitch-1 {
            0%, 100% {
                clip-path: inset(0 0 0 0);
                transform: translate(0);
            }
            20% {
                clip-path: inset(33% 0 0 0);
                transform: translate(-2px);
            }
            40% {
                clip-path: inset(0 0 55% 0);
                transform: translate(2px);
            }
            60% {
                clip-path: inset(0 0 0 0);
                transform: translate(-1px);
            }
            80% {
                clip-path: inset(25% 0 0 0);
                transform: translate(1px);
            }
        }
        
        @keyframes glitch-2 {
            0%, 100% {
                clip-path: inset(0 0 0 0);
                transform: translate(0);
            }
            20% {
                clip-path: inset(0 0 70% 0);
                transform: translate(2px);
            }
            40% {
                clip-path: inset(40% 0 0 0);
                transform: translate(-2px);
            }
            60% {
                clip-path: inset(0 0 0 0);
                transform: translate(1px);
            }
            80% {
                clip-path: inset(0 0 35% 0);
                transform: translate(-1px);
            }
        }
    `;

  document.head.appendChild(style);
}

// Initialize animations on page load
document.addEventListener("DOMContentLoaded", () => {
  // Add glitch effect to hero title
  const heroTitle = document.querySelector(".hero-title");
  if (heroTitle) {
    setTimeout(() => {
      addGlitchEffect(heroTitle);
    }, 1000);
  }

  // Initialize reveal animations
  const revealElements = document.querySelectorAll(
    ".feature-card, .step, .testimonial"
  );
  revealElements.forEach((el) => el.classList.add("reveal"));
});
