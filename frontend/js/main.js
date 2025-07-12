// API Configuration
const API_BASE_URL = "http://localhost:5000/api";

// DOM Elements
const navbar = document.getElementById("navbar");
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const registerForm = document.getElementById("registerForm");

// Global variables
let stream = null;
let capturedImage = null;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  initializeApp();
});

function initializeApp() {
  // Setup event listeners
  setupEventListeners();

  // Start camera for register section
  startCamera();

  // Load today's attendance
  loadTodayAttendance();

  // Initialize particles
  initParticles();
}

// Event Listeners
function setupEventListeners() {
  // Navbar scroll effect
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // Hamburger menu
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navLinks.classList.toggle("active");
  });

  // Nav links click
  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      hamburger.classList.remove("active");
      navLinks.classList.remove("active");
    });
  });

  // Register form submission
  registerForm.addEventListener("submit", handleRegistration);

  // Smooth scrolling
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// Camera Functions
async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "user",
      },
    });
    video.srcObject = stream;
  } catch (err) {
    console.error("Error accessing camera:", err);
    showNotification(
      "Camera access denied. Please enable camera permissions.",
      "error"
    );
  }
}

function captureImage() {
  if (!stream) {
    showNotification("Camera not initialized", "error");
    return;
  }

  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0);

  capturedImage = canvas.toDataURL("image/jpeg");

  // Visual feedback
  const overlay = document.querySelector(".camera-overlay");
  overlay.style.borderColor = "#00ff00";
  setTimeout(() => {
    overlay.style.borderColor = "var(--cyan-glow)";
  }, 500);

  showNotification("Photo captured successfully!", "success");
}

// Registration Handler
async function handleRegistration(e) {
  e.preventDefault();

  if (!capturedImage) {
    showNotification("Please capture a photo first", "error");
    return;
  }

  const name = document.getElementById("name").value;
  const studentId = document.getElementById("studentId").value;

  // Show loading
  showLoading(true);

  try {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        student_id: studentId,
        image: capturedImage,
      }),
    });

    const data = await response.json();

    if (data.success) {
      showNotification("Registration successful!", "success");
      registerForm.reset();
      capturedImage = null;
    } else {
      showNotification(data.message || "Registration failed", "error");
    }
  } catch (error) {
    console.error("Registration error:", error);
    showNotification("Registration failed. Please try again.", "error");
  } finally {
    showLoading(false);
  }
}

// Attendance Functions
async function loadTodayAttendance() {
  try {
    const response = await fetch(`${API_BASE_URL}/attendance/today`);
    const data = await response.json();

    if (data.success) {
      displayAttendance(data.records);
    }
  } catch (error) {
    console.error("Error loading attendance:", error);
  }
}

function displayAttendance(records) {
  const attendanceList = document.getElementById("attendanceList");
  attendanceList.innerHTML = "";

  if (records.length === 0) {
    attendanceList.innerHTML =
      '<p style="text-align: center; opacity: 0.6;">No attendance records for today</p>';
    return;
  }

  records.forEach((record) => {
    const item = document.createElement("div");
    item.className = "attendance-item";
    item.innerHTML = `
            <h4>${record.name}</h4>
            <p>ID: ${record.student_id}</p>
            <p>Time: ${formatTime(record.timestamp)}</p>
        `;
    attendanceList.appendChild(item);
  });
}

// Utility Functions
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function showNotification(message, type = "info") {
  // Create notification element
  const notification = document.createElement("div");
  notification.className = `notification ${type}`;
  notification.innerHTML = `
        <i class="fas fa-${
          type === "success" ? "check-circle" : "exclamation-circle"
        }"></i>
        <span>${message}</span>
    `;

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
        .notification {
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 20px;
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 2000;
            animation: slideIn 0.3s ease;
        }
        
        .notification.success {
            border-color: #00ff00;
            color: #00ff00;
        }
        
        .notification.error {
            border-color: #ff0000;
            color: #ff0000;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;

  document.head.appendChild(style);
  document.body.appendChild(notification);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease";
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 3000);
}

function showLoading(show) {
  const submitBtn = document.querySelector(".submit-btn");
  if (show) {
    submitBtn.disabled = true;
    submitBtn.innerHTML =
      '<i class="fas fa-spinner fa-spin"></i> Processing...';
  } else {
    submitBtn.disabled = false;
    submitBtn.innerHTML = "Register Face";
  }
}

function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
}

// Demo Function
function startDemo() {
  showNotification("Demo mode activated! Exploring features...", "success");

  // Simulate navigation through sections
  const sections = ["features", "register", "dashboard"];
  let index = 0;

  const interval = setInterval(() => {
    if (index < sections.length) {
      scrollToSection(sections[index]);
      index++;
    } else {
      clearInterval(interval);
      showNotification("Demo completed!", "success");
    }
  }, 3000);
}

// Initialize Particles.js
function initParticles() {
  if (typeof particlesJS !== "undefined") {
    particlesJS("particles-js", {
      particles: {
        number: {
          value: 80,
          density: {
            enable: true,
            value_area: 800,
          },
        },
        color: {
          value: "#00d4ff",
        },
        shape: {
          type: "circle",
        },
        opacity: {
          value: 0.5,
          random: false,
        },
        size: {
          value: 3,
          random: true,
        },
        line_linked: {
          enable: true,
          distance: 150,
          color: "#00d4ff",
          opacity: 0.4,
          width: 1,
        },
        move: {
          enable: true,
          speed: 2,
          direction: "none",
          random: false,
          straight: false,
          out_mode: "out",
          bounce: false,
        },
      },
      interactivity: {
        detect_on: "canvas",
        events: {
          onhover: {
            enable: true,
            mode: "grab",
          },
          onclick: {
            enable: true,
            mode: "push",
          },
          resize: true,
        },
        modes: {
          grab: {
            distance: 140,
            line_linked: {
              opacity: 1,
            },
          },
          push: {
            particles_nb: 4,
          },
        },
      },
      retina_detect: true,
    });
  }
}

// Auto-refresh attendance every 30 seconds
setInterval(loadTodayAttendance, 30000);
