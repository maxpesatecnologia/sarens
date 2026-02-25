/* ============================================================
   SARENS — Main JS (Parallax, Cursor, Loader, Animations)
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── AOS Init ────────────────────────────────────────
  AOS.init({
    once: true,
    offset: 60,
    duration: 800,
    easing: 'ease-out-cubic',
  });

  // ── Loader ──────────────────────────────────────────
  const loader = document.getElementById('loader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        loader.classList.add('hidden');
        document.body.style.overflow = '';
      }, 1900);
    });
    document.body.style.overflow = 'hidden';
  }

  // ── Custom Cursor ────────────────────────────────────
  const cursor = document.querySelector('.cursor');
  const cursorFollower = document.querySelector('.cursor-follower');
  let mouseX = 0, mouseY = 0;
  let followerX = 0, followerY = 0;

  if (cursor && cursorFollower) {
    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = mouseX + 'px';
      cursor.style.top = mouseY + 'px';
    });

    function animateFollower() {
      followerX += (mouseX - followerX) * 0.12;
      followerY += (mouseY - followerY) * 0.12;
      cursorFollower.style.left = followerX + 'px';
      cursorFollower.style.top = followerY + 'px';
      requestAnimationFrame(animateFollower);
    }
    animateFollower();

    // Hover effects on interactive elements
    const interactives = document.querySelectorAll('a, button, .service-card, .fleet-card, .fleet-item-card, .filter-btn');
    interactives.forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.style.width = '18px';
        cursor.style.height = '18px';
        cursor.style.background = 'transparent';
        cursor.style.border = '2px solid #C8A84B';
        cursorFollower.style.width = '54px';
        cursorFollower.style.height = '54px';
        cursorFollower.style.opacity = '1';
      });
      el.addEventListener('mouseleave', () => {
        cursor.style.width = '10px';
        cursor.style.height = '10px';
        cursor.style.background = '#C8A84B';
        cursor.style.border = 'none';
        cursorFollower.style.width = '36px';
        cursorFollower.style.height = '36px';
        cursorFollower.style.opacity = '0.5';
      });
    });
  }

  // ── Navbar Scroll Behavior ───────────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // ── Mobile Menu ──────────────────────────────────────
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileClose = document.getElementById('mobileClose');
  const mobileOverlay = document.getElementById('mobileOverlay');

  function openMenu() {
    mobileMenu.classList.add('open');
    mobileOverlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    mobileMenu.classList.remove('open');
    mobileOverlay.classList.remove('show');
    document.body.style.overflow = '';
  }

  if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openMenu);
  if (mobileClose) mobileClose.addEventListener('click', closeMenu);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeMenu);

  // ── Parallax Hero ────────────────────────────────────
  const heroParallax = document.getElementById('heroParallax');
  if (heroParallax) {
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY;
      heroParallax.style.transform = `translateY(${scrolled * 0.35}px)`;
    }, { passive: true });
  }

  // ── Parallax Divider ─────────────────────────────────
  const parallaxDividers = document.querySelectorAll('.parallax-divider-bg');
  if (parallaxDividers.length) {
    const parallaxObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          window.addEventListener('scroll', updateParallaxDividers, { passive: true });
        }
      });
    });
    parallaxDividers.forEach(d => parallaxObserver.observe(d));

    function updateParallaxDividers() {
      parallaxDividers.forEach(bg => {
        const section = bg.closest('.parallax-divider');
        if (!section) return;
        const rect = section.getBoundingClientRect();
        const scrollProgress = -rect.top / (rect.height + window.innerHeight);
        const offset = scrollProgress * 80;
        bg.style.transform = `translateY(${offset}px) scale(1.15)`;
      });
    }
  }

  // ── Counter Animation ────────────────────────────────
  const statNumbers = document.querySelectorAll('.stat-number[data-target]');

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.target);
        const duration = 2000;
        const start = performance.now();

        function update(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 4);
          el.textContent = Math.floor(eased * target).toLocaleString('pt-BR');
          if (progress < 1) requestAnimationFrame(update);
          else el.textContent = target.toLocaleString('pt-BR');
        }
        requestAnimationFrame(update);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(n => counterObserver.observe(n));

  // ── Fleet Filter ─────────────────────────────────────
  const filterBtns = document.querySelectorAll('.filter-btn');
  const fleetItems = document.querySelectorAll('.fleet-item-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;
      fleetItems.forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.classList.remove('hidden');
          item.style.animation = 'none';
          requestAnimationFrame(() => {
            item.style.animation = '';
          });
        } else {
          item.classList.add('hidden');
        }
      });
    });
  });

  // ── Form Submit ──────────────────────────────────────
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = contactForm.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.innerHTML = '<i class="ph ph-check-circle"></i> Enviado com sucesso!';
      btn.style.background = '#16A34A';
      btn.disabled = true;
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = '';
        btn.disabled = false;
        contactForm.reset();
      }, 4000);
    });
  }

  // ── Smooth Hover Cards ───────────────────────────────
  const hoverCards = document.querySelectorAll('.service-card, .mvv-card, .fleet-item-card');
  hoverCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `translateY(-6px) rotateX(${-y * 4}deg) rotateY(${x * 4}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  // ── Active Nav Link on page ──────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') && currentPath.includes(link.getAttribute('href').replace('./', ''))) {
      link.classList.add('active');
    }
  });

  // ── WhatsApp Float Button (inject) ──────────────────
  const wa = document.createElement('a');
  wa.href = 'https://wa.me/5511999999999';
  wa.target = '_blank';
  wa.className = 'whatsapp-float';
  wa.innerHTML = '<i class="ph ph-whatsapp-logo"></i>';
  wa.title = 'Fale conosco no WhatsApp';
  document.body.appendChild(wa);

  // Style inject
  const style = document.createElement('style');
  style.textContent = `
    .whatsapp-float {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      width: 56px;
      height: 56px;
      background: #25D366;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 1.8rem;
      box-shadow: 0 8px 24px rgba(37,211,102,0.4);
      z-index: 999;
      transition: all 0.3s cubic-bezier(0.25,0.8,0.25,1);
      animation: waPulse 2.5s ease-in-out infinite;
    }
    .whatsapp-float:hover {
      transform: scale(1.1);
      box-shadow: 0 12px 32px rgba(37,211,102,0.5);
    }
    @keyframes waPulse {
      0%, 100% { box-shadow: 0 8px 24px rgba(37,211,102,0.4), 0 0 0 0 rgba(37,211,102,0.3); }
      50% { box-shadow: 0 8px 24px rgba(37,211,102,0.4), 0 0 0 12px rgba(37,211,102,0); }
    }
    @keyframes cardFadeIn {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .fleet-item-card { animation: cardFadeIn 0.35s ease-out forwards; }
  `;
  document.head.appendChild(style);

  // ── Reveal progress bar on hero eyebrow ─────────────
  const eyebrow = document.querySelector('.hero-eyebrow');
  if (eyebrow) {
    eyebrow.style.opacity = '0';
    eyebrow.style.transform = 'translateY(-10px)';
    setTimeout(() => {
      eyebrow.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
      eyebrow.style.opacity = '1';
      eyebrow.style.transform = 'translateY(0)';
    }, 2000);
  }

});
