/**
 * LUMIÈRE LASH & BROW - Interactive Master Script
 * Handles Navigation Drawer, Theme (Dark/Light), Direction (RTL/LTR),
 * Before/After Comparison Slider, and Accessibility.
 */

document.addEventListener('DOMContentLoaded', () => {
  // --------------------------------------------------------------------------
  // 1. THEME MANAGEMENT (Dark / Light Mode)
  // --------------------------------------------------------------------------
  const themeToggleDesktop = document.getElementById('themeToggleDesktop');
  const themeToggleMobile = document.getElementById('themeToggleMobile');
  const htmlRoot = document.documentElement;
  
  // Check stored theme or system preference
  const savedTheme = localStorage.getItem('lumiere-theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme) {
    applyTheme(savedTheme);
  } else if (systemPrefersDark) {
    applyTheme('dark');
  } else {
    applyTheme('light');
  }

  function applyTheme(theme) {
    htmlRoot.setAttribute('data-theme', theme);
    localStorage.setItem('lumiere-theme', theme);
    updateThemeIcons(theme);
  }

  function toggleTheme() {
    const currentTheme = htmlRoot.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
  }

  function updateThemeIcons(theme) {
    const isDark = theme === 'dark';
    
    // Desktop icon
    if (themeToggleDesktop) {
      const icon = themeToggleDesktop.querySelector('i');
      if (icon) {
        icon.className = isDark ? 'bi bi-sun' : 'bi bi-moon-stars';
      }
      themeToggleDesktop.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    }

    // Mobile drawer toggle text & icon
    if (themeToggleMobile) {
      const icon = themeToggleMobile.querySelector('i');
      const text = themeToggleMobile.querySelector('.toggle-label');
      if (icon) {
        icon.className = isDark ? 'bi bi-sun' : 'bi bi-moon-stars';
      }
      if (text) {
        text.textContent = isDark ? 'Light Mode' : 'Dark Mode';
      }
      themeToggleMobile.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    }
  }

  if (themeToggleDesktop) {
    themeToggleDesktop.addEventListener('click', toggleTheme);
  }
  if (themeToggleMobile) {
    themeToggleMobile.addEventListener('click', toggleTheme);
  }

  // --------------------------------------------------------------------------
  // 2. DIRECTION MANAGEMENT (RTL / LTR)
  // --------------------------------------------------------------------------
  const rtlToggleDesktop = document.getElementById('rtlToggleDesktop');
  const rtlToggleMobile = document.getElementById('rtlToggleMobile');

  const savedDir = localStorage.getItem('lumiere-dir') || 'ltr';
  applyDirection(savedDir);

  function applyDirection(dir) {
    htmlRoot.setAttribute('dir', dir);
    localStorage.setItem('lumiere-dir', dir);
    updateRtlButtons(dir);
  }

  function toggleDirection() {
    const currentDir = htmlRoot.getAttribute('dir') || 'ltr';
    const newDir = currentDir === 'rtl' ? 'ltr' : 'rtl';
    applyDirection(newDir);
  }

  function updateRtlButtons(dir) {
    const isRtl = dir === 'rtl';
    const label = isRtl ? 'Switch to LTR' : 'Switch to RTL';
    
    if (rtlToggleDesktop) {
      rtlToggleDesktop.setAttribute('aria-label', label);
    }
    if (rtlToggleMobile) {
      rtlToggleMobile.setAttribute('aria-label', label);
      const text = rtlToggleMobile.querySelector('.toggle-label');
      if (text) {
        text.textContent = isRtl ? 'LTR View' : 'RTL View';
      }
    }
  }

  if (rtlToggleDesktop) {
    rtlToggleDesktop.addEventListener('click', toggleDirection);
  }
  if (rtlToggleMobile) {
    rtlToggleMobile.addEventListener('click', toggleDirection);
  }

  // --------------------------------------------------------------------------
  // 3. MOBILE & TABLET DRAWER NAVIGATION
  // --------------------------------------------------------------------------
  const btnHamburger = document.getElementById('btnHamburger');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerBackdrop = document.getElementById('drawerBackdrop');
  const btnDrawerClose = document.getElementById('btnDrawerClose');
  const drawerLinks = document.querySelectorAll('.mobile-drawer a:not(.drawer-accordion-btn)');

  function openDrawer() {
    if (!mobileDrawer || !drawerBackdrop) return;
    mobileDrawer.classList.add('active');
    drawerBackdrop.classList.add('active');
    document.body.classList.add('drawer-open');
    if (btnHamburger) btnHamburger.setAttribute('aria-expanded', 'true');
    if (btnDrawerClose) btnDrawerClose.focus();
  }

  function closeDrawer() {
    if (!mobileDrawer || !drawerBackdrop) return;
    mobileDrawer.classList.remove('active');
    drawerBackdrop.classList.remove('active');
    document.body.classList.remove('drawer-open');
    if (btnHamburger) {
      btnHamburger.setAttribute('aria-expanded', 'false');
      btnHamburger.focus();
    }
  }

  if (btnHamburger) btnHamburger.addEventListener('click', openDrawer);
  if (btnDrawerClose) btnDrawerClose.addEventListener('click', closeDrawer);
  if (drawerBackdrop) drawerBackdrop.addEventListener('click', closeDrawer);

  // Close drawer when clicking any regular link inside
  drawerLinks.forEach(link => {
    link.addEventListener('click', () => {
      closeDrawer();
    });
  });

  // Drawer Home Accordion
  const drawerHomeAccordionBtn = document.getElementById('drawerHomeAccordionBtn');
  const drawerHomeAccordionContent = document.getElementById('drawerHomeAccordionContent');

  if (drawerHomeAccordionBtn && drawerHomeAccordionContent) {
    drawerHomeAccordionBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const isOpen = drawerHomeAccordionContent.classList.contains('open');
      if (isOpen) {
        drawerHomeAccordionContent.classList.remove('open');
        drawerHomeAccordionBtn.setAttribute('aria-expanded', 'false');
      } else {
        drawerHomeAccordionContent.classList.add('open');
        drawerHomeAccordionBtn.setAttribute('aria-expanded', 'true');
      }
    });
  }

  // Keyboard accessibility (Escape key to close drawer)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileDrawer && mobileDrawer.classList.contains('active')) {
      closeDrawer();
    }
  });

  // --------------------------------------------------------------------------
  // 4. INTERACTIVE BEFORE / AFTER SLIDER
  // --------------------------------------------------------------------------
  const baViewer = document.getElementById('baViewer');
  const baLayerAfter = document.getElementById('baLayerAfter');
  const baHandle = document.getElementById('baHandle');

  if (baViewer && baLayerAfter && baHandle) {
    let isDragging = false;

    const setPosition = (clientX) => {
      const rect = baViewer.getBoundingClientRect();
      const isRTL = htmlRoot.getAttribute('dir') === 'rtl';
      let x = clientX - rect.left;
      
      x = Math.max(0, Math.min(x, rect.width));
      let percentage = (x / rect.width) * 100;

      if (isRTL) {
        baLayerAfter.style.width = `${100 - percentage}%`;
        baHandle.style.left = `${percentage}%`;
      } else {
        baLayerAfter.style.width = `${percentage}%`;
        baHandle.style.left = `${percentage}%`;
      }
    };

    const onPointerDown = (e) => {
      isDragging = true;
      setPosition(e.clientX || (e.touches && e.touches[0].clientX));
    };

    const onPointerMove = (e) => {
      if (!isDragging) return;
      setPosition(e.clientX || (e.touches && e.touches[0].clientX));
    };

    const onPointerUp = () => {
      isDragging = false;
    };

    baViewer.addEventListener('mousedown', onPointerDown);
    window.addEventListener('mousemove', onPointerMove);
    window.addEventListener('mouseup', onPointerUp);

    baViewer.addEventListener('touchstart', onPointerDown, { passive: true });
    window.addEventListener('touchmove', onPointerMove, { passive: true });
    window.addEventListener('touchend', onPointerUp);

    // Keyboard support for before/after handle
    baHandle.addEventListener('keydown', (e) => {
      let currentWidth = parseFloat(baLayerAfter.style.width) || 50;
      if (e.key === 'ArrowLeft') {
        currentWidth = Math.max(0, currentWidth - 5);
      } else if (e.key === 'ArrowRight') {
        currentWidth = Math.min(100, currentWidth + 5);
      } else {
        return;
      }
      baLayerAfter.style.width = `${currentWidth}%`;
      baHandle.style.left = `${currentWidth}%`;
    });
  }

  // --------------------------------------------------------------------------
  // 5. ACCESSIBLE GALLERY LIGHTBOX
  // --------------------------------------------------------------------------
  const lightboxModal = document.getElementById('galleryLightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxCounter = document.getElementById('lightboxCounter');
  const lightboxClose = document.getElementById('lightboxClose');
  const lightboxPrev = document.getElementById('lightboxPrev');
  const lightboxNext = document.getElementById('lightboxNext');
  const galleryTriggers = Array.from(document.querySelectorAll('[data-lightbox-src]'));

  let currentGalleryIndex = 0;
  let lastActiveTrigger = null;

  if (lightboxModal && galleryTriggers.length > 0) {
    function openLightbox(index) {
      if (index < 0 || index >= galleryTriggers.length) return;
      currentGalleryIndex = index;
      const trigger = galleryTriggers[index];
      lastActiveTrigger = trigger;

      const src = trigger.getAttribute('data-lightbox-src') || trigger.querySelector('img')?.src;
      const caption = trigger.getAttribute('data-lightbox-caption') || trigger.querySelector('img')?.alt || 'Lumière Beauty Look';

      if (lightboxImg) {
        lightboxImg.src = src;
        lightboxImg.alt = caption;
      }
      if (lightboxTitle) {
        lightboxTitle.textContent = caption;
      }
      if (lightboxCounter) {
        lightboxCounter.textContent = `${index + 1} of ${galleryTriggers.length}`;
      }

      lightboxModal.classList.add('active');
      lightboxModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      if (lightboxClose) lightboxClose.focus();
    }

    function closeLightbox() {
      lightboxModal.classList.remove('active');
      lightboxModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastActiveTrigger) lastActiveTrigger.focus();
    }

    function showPrev() {
      const newIndex = (currentGalleryIndex - 1 + galleryTriggers.length) % galleryTriggers.length;
      openLightbox(newIndex);
    }

    function showNext() {
      const newIndex = (currentGalleryIndex + 1) % galleryTriggers.length;
      openLightbox(newIndex);
    }

    galleryTriggers.forEach((trigger, idx) => {
      trigger.setAttribute('tabindex', '0');
      trigger.setAttribute('role', 'button');
      trigger.setAttribute('aria-label', `View larger image: ${trigger.getAttribute('data-lightbox-caption') || 'Lumière Look'}`);

      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        openLightbox(idx);
      });

      trigger.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLightbox(idx);
        }
      });
    });

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxPrev) lightboxPrev.addEventListener('click', showPrev);
    if (lightboxNext) lightboxNext.addEventListener('click', showNext);

    lightboxModal.addEventListener('click', (e) => {
      if (e.target === lightboxModal || e.target.classList.contains('lightbox-content-wrap')) {
        closeLightbox();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (!lightboxModal.classList.contains('active')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') {
        const isRtl = htmlRoot.getAttribute('dir') === 'rtl';
        isRtl ? showNext() : showPrev();
      }
      if (e.key === 'ArrowRight') {
        const isRtl = htmlRoot.getAttribute('dir') === 'rtl';
        isRtl ? showPrev() : showNext();
      }
    });
  }

  // --------------------------------------------------------------------------
  // 6. ACCESSIBLE CONTACT FAQ ACCORDION
  // --------------------------------------------------------------------------
  const faqButtons = document.querySelectorAll('.faq-accordion-header');
  
  faqButtons.forEach(button => {
    button.addEventListener('click', () => {
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      const targetId = button.getAttribute('aria-controls');
      const targetContent = document.getElementById(targetId);

      // Close all other accordions for clean single-view accordion
      faqButtons.forEach(otherBtn => {
        if (otherBtn !== button) {
          otherBtn.setAttribute('aria-expanded', 'false');
          const otherId = otherBtn.getAttribute('aria-controls');
          const otherContent = document.getElementById(otherId);
          if (otherContent) {
            otherContent.classList.remove('open');
          }
        }
      });

      if (isExpanded) {
        button.setAttribute('aria-expanded', 'false');
        if (targetContent) targetContent.classList.remove('open');
      } else {
        button.setAttribute('aria-expanded', 'true');
        if (targetContent) targetContent.classList.add('open');
      }
    });
  });

  // --------------------------------------------------------------------------
  // 7. URL PARAMETER PRE-SELECTION & SMOOTH CTA ROUTING
  // --------------------------------------------------------------------------
  const bookingServiceSelect = document.getElementById('bookingService');
  const bookingSection = document.getElementById('booking');

  // Parse URL search params for pre-selected service
  const urlParams = new URLSearchParams(window.location.search);
  const requestedService = urlParams.get('service');

  if (requestedService && bookingServiceSelect) {
    const serviceSearch = decodeURIComponent(requestedService).toLowerCase();
    for (let i = 0; i < bookingServiceSelect.options.length; i++) {
      const optVal = bookingServiceSelect.options[i].value.toLowerCase();
      const optText = bookingServiceSelect.options[i].text.toLowerCase();
      if (optVal.includes(serviceSearch) || serviceSearch.includes(optVal) || optText.includes(serviceSearch)) {
        bookingServiceSelect.selectedIndex = i;
        break;
      }
    }
  }

  // Smooth scroll to #booking if hash or service param is present on page load
  if (window.location.hash === '#booking' || (requestedService && bookingSection)) {
    setTimeout(() => {
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        const nameInput = document.getElementById('bookingName');
        if (nameInput) {
          setTimeout(() => nameInput.focus(), 500);
        }
      }
    }, 150);
  }

  // Handle in-page smooth scrolls for any Book an Appointment CTA links on contact.html
  const bookingCtaLinks = document.querySelectorAll('a[href="#booking"], a[href="contact.html#booking"], a[href^="contact.html?service="]');
  bookingCtaLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const isContactPage = window.location.pathname.endsWith('contact.html') || (!window.location.pathname.includes('.html') && document.getElementById('bookingForm'));
      if (isContactPage && bookingSection) {
        const targetHref = link.getAttribute('href') || '';
        // If it specifies a service query param in the link on the same page
        if (targetHref.includes('service=') && bookingServiceSelect) {
          const match = targetHref.match(/service=([^#&]+)/);
          if (match && match[1]) {
            const svc = decodeURIComponent(match[1]).toLowerCase();
            for (let i = 0; i < bookingServiceSelect.options.length; i++) {
              if (bookingServiceSelect.options[i].value.toLowerCase().includes(svc) || svc.includes(bookingServiceSelect.options[i].value.toLowerCase())) {
                bookingServiceSelect.selectedIndex = i;
                break;
              }
            }
          }
        }
        e.preventDefault();
        bookingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        const nameInput = document.getElementById('bookingName');
        if (nameInput) {
          setTimeout(() => nameInput.focus(), 400);
        }
      }
    });
  });

  // --------------------------------------------------------------------------
  // 8. CONTACT / BOOKING FORM VALIDATION & FEEDBACK
  // --------------------------------------------------------------------------
  const bookingForm = document.getElementById('bookingForm');
  const bookingStatusMessage = document.getElementById('bookingStatusMessage');

  if (bookingForm && bookingStatusMessage) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Clear previous error states
      const formControls = bookingForm.querySelectorAll('.form-control-lumiere');
      formControls.forEach(ctrl => ctrl.classList.remove('is-invalid'));

      let isValid = true;
      const requiredInputs = bookingForm.querySelectorAll('[required]');

      requiredInputs.forEach(input => {
        if (!input.value.trim()) {
          input.classList.add('is-invalid');
          isValid = false;
        } else if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim())) {
          input.classList.add('is-invalid');
          isValid = false;
        }
      });

      if (!isValid) {
        bookingStatusMessage.className = 'booking-status-alert alert-error';
        bookingStatusMessage.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i> Please complete all required fields with valid details so our studio team can arrange your appointment.';
        bookingStatusMessage.style.display = 'block';
        bookingStatusMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        return;
      }

      // Collect submitted values for transparent confirmation
      const clientName = document.getElementById('bookingName')?.value.trim() || 'Guest';
      const clientService = document.getElementById('bookingService')?.value || 'Selected Service';
      const clientDate = document.getElementById('bookingDate')?.value || 'Preferred Date';
      const clientTime = document.getElementById('bookingTime')?.value || 'Preferred Time';

      bookingStatusMessage.className = 'booking-status-alert alert-success';
      bookingStatusMessage.innerHTML = `
        <div style="display: flex; gap: 0.8rem; align-items: flex-start;">
          <i class="bi bi-check-circle-fill" style="font-size: 1.35rem; color: var(--color-primary); flex-shrink: 0; margin-top: 0.15rem;"></i>
          <div>
            <strong style="font-size: 1.05rem; display: block; margin-bottom: 0.35rem;">Thank you, ${clientName}! Your appointment inquiry has been received.</strong>
            <p style="margin: 0 0 0.5rem; opacity: 0.95;">
              We have noted your request for <strong>${clientService}</strong> on <strong>${clientDate}</strong> (${clientTime}).
            </p>
            <p style="margin: 0; font-size: 0.88rem; opacity: 0.85;">
              A member of the LUMIÈRE studio team will connect with you promptly to confirm availability and finalize your booking.
            </p>
          </div>
        </div>
      `;
      bookingStatusMessage.style.display = 'block';
      bookingForm.reset();
      bookingStatusMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  }

  // --------------------------------------------------------------------------
  // 9. LASH STYLE FILTER PILLS (services.html)
  // --------------------------------------------------------------------------
  const filterPills = document.querySelectorAll('.btn-filter-pill');
  const serviceCards = document.querySelectorAll('.service-detail-card');

  if (filterPills.length > 0 && serviceCards.length > 0) {
    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');

        const filter = pill.getAttribute('data-filter');

        serviceCards.forEach(card => {
          const style = card.getAttribute('data-style');
          if (filter === 'all' || style === filter) {
            card.classList.remove('card-dimmed');
            if (filter !== 'all') {
              card.classList.add('card-highlighted');
            } else {
              card.classList.remove('card-highlighted');
            }
          } else {
            card.classList.add('card-dimmed');
            card.classList.remove('card-highlighted');
          }
        });
      });
    });
  }
});


