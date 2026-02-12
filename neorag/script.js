// === Particles Background ===
// (keep this part exactly the same as before)

const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
let particlesArray = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class Particle {
  constructor() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size = Math.random() * 3 + 1;
    this.speedX = Math.random() * 0.8 - 0.4;
    this.speedY = Math.random() * 0.8 - 0.4;
  }
  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
    if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
  }
  draw() {
    ctx.fillStyle = 'rgba(0,240,255,0.6)';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

function initParticles() {
  particlesArray = [];
  for (let i = 0; i < 80; i++) {
    particlesArray.push(new Particle());
  }
}

function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particlesArray.forEach(p => {
    p.update();
    p.draw();
  });
  requestAnimationFrame(animateParticles);
}

initParticles();
animateParticles();

// === Real Backend Integration ===

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('pdf-upload');
const fileInfo = document.getElementById('file-info');
const uploadSection = document.getElementById('upload-section');
const chatSection = document.getElementById('chat-section');
const loadingOverlay = document.getElementById('loading');
const messages = document.getElementById('messages');
const questionInput = document.getElementById('question-input');
const sendBtn = document.getElementById('send-btn');

const API_BASE = 'http://localhost:5000';  // Flask runs on port 5000

function showLoading() {
  loadingOverlay.style.display = 'flex';
}

function hideLoading() {
  loadingOverlay.style.display = 'none';
}

function addMessage(content, isUser = false) {
  const msg = document.createElement('div');
  msg.classList.add('message');
  msg.classList.add(isUser ? 'user' : 'assistant');
  msg.textContent = content;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}

function addLoadingBubble() {
  const bubble = document.createElement('div');
  bubble.classList.add('message', 'assistant', 'loading');
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}

function removeLoadingBubble(bubble) {
  if (bubble && bubble.parentNode) bubble.remove();
}

// Drag & Drop
['dragover', 'dragenter'].forEach(evt => {
  dropZone.addEventListener(evt, e => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });
});

['dragleave', 'drop'].forEach(evt => {
  dropZone.addEventListener(evt, e => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
  });
});

dropZone.addEventListener('drop', e => {
  const file = e.dataTransfer.files[0];
  if (file && file.type === 'application/pdf') {
    handleFile(file);
  }
});

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) handleFile(file);
});

async function handleFile(file) {
  fileInfo.textContent = `Selected: ${file.name}`;
  showLoading();

  const formData = new FormData();
  formData.append('pdf', file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    hideLoading();

    if (!res.ok || !data.success) {
      addMessage("Error: " + (data.error || "Failed to process PDF"), false);
      return;
    }

    // Success
    uploadSection.style.display = 'none';
    chatSection.style.display = 'flex';

    addMessage(`Document "${file.name}" successfully indexed.`, false);
    addMessage("You can now ask questions about the content.", false);

  } catch (err) {
    hideLoading();
    addMessage("Network error while uploading. Is the backend running?", false);
  }
}

async function askQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  addMessage(question, true);
  questionInput.value = '';
  sendBtn.disabled = true;

  const loadingBubble = addLoadingBubble();

  try {
    const res = await fetch(`${API_BASE}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    removeLoadingBubble(loadingBubble);

    if (res.ok && data.success) {
      addMessage(data.answer, false);
    } else {
      addMessage("Error: " + (data.error || "Something went wrong"), false);
    }

  } catch (err) {
    removeLoadingBubble(loadingBubble);
    addMessage("Failed to connect to the server. Is Flask running?", false);
  }

  sendBtn.disabled = false;
}

sendBtn.addEventListener('click', askQuestion);

questionInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    askQuestion();
  }
});

questionInput.addEventListener('input', () => {
  sendBtn.disabled = !questionInput.value.trim();
});