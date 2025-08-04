// ===== GLOBAL THEME FUNCTIONALITY =====

class Theme {
  constructor() {
    this.init();
  }

  init() {
    this.initSmoothScrolling();
    this.initScrollAnimations();
    this.initStickyMobileCTA();
    this.initVideoAutoplay();
    this.initAnalytics();
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        this.onDOMReady();
      });
    } else {
      this.onDOMReady();
    }
  }

  onDOMReady() {
    this.initLazyLoading();
    this.initFormValidation();
    this.trackPageView();
  }

  // ===== SMOOTH SCROLLING =====
  initSmoothScrolling() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href^="#"]');
      if (!link) return;

      const targetId = link.getAttribute('href');
      if (targetId === '#') return;

      const targetElement = document.querySelector(targetId);
      if (!targetElement) return;

      e.preventDefault();
      
      const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
      const targetPosition = targetElement.offsetTop - headerHeight - 20;

      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });

      // Track click event
      this.trackEvent('Navigation', 'Smooth Scroll', targetId);
    });
  }

  // ===== SCROLL ANIMATIONS =====
  initScrollAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-on-scroll');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.benefit-card, .review-card, .bundle-card, .faq-item');
    animateElements.forEach(el => observer.observe(el));
  }

  // ===== STICKY MOBILE CTA =====
  initStickyMobileCTA() {
    const stickyCTA = document.querySelector('.sticky-mobile-cta');
    const buyNowSection = document.querySelector('#buy-now');
    
    if (!stickyCTA || !buyNowSection) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          stickyCTA.style.transform = 'translateY(100%)';
        } else {
          stickyCTA.style.transform = 'translateY(0)';
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(buyNowSection);

    // Track sticky CTA clicks
    stickyCTA.addEventListener('click', () => {
      this.trackEvent('CTA', 'Sticky Mobile Click', 'Buy Now');
    });
  }

  // ===== VIDEO AUTOPLAY =====
  initVideoAutoplay() {
    const videos = document.querySelectorAll('video[autoplay]');
    
    videos.forEach(video => {
      // Intersection observer for video autoplay
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            video.play().catch(e => console.log('Video autoplay prevented:', e));
          } else {
            video.pause();
          }
        },
        { threshold: 0.5 }
      );

      observer.observe(video);

      // Track video engagement
      video.addEventListener('play', () => {
        this.trackEvent('Video', 'Play', 'Product Demo');
      });

      video.addEventListener('ended', () => {
        this.trackEvent('Video', 'Complete', 'Product Demo');
      });
    });
  }

  // ===== LAZY LOADING =====
  initLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src || img.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
          }
        });
      });

      images.forEach(img => imageObserver.observe(img));
    }
  }

  // ===== FORM VALIDATION =====
  initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        if (!this.validateForm(form)) {
          e.preventDefault();
          return false;
        }
        
        this.trackEvent('Form', 'Submit', form.getAttribute('action') || 'Unknown');
      });
    });
  }

  validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
      if (!field.value.trim()) {
        this.showFieldError(field, 'This field is required');
        isValid = false;
      } else if (field.type === 'email' && !this.isValidEmail(field.value)) {
        this.showFieldError(field, 'Please enter a valid email address');
        isValid = false;
      } else {
        this.clearFieldError(field);
      }
    });

    return isValid;
  }

  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  showFieldError(field, message) {
    this.clearFieldError(field);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.color = 'var(--color-error)';
    errorElement.style.fontSize = '0.875rem';
    errorElement.style.marginTop = '0.25rem';
    
    field.parentNode.appendChild(errorElement);
    field.style.borderColor = 'var(--color-error)';
  }

  clearFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
      existingError.remove();
    }
    field.style.borderColor = '';
  }

  // ===== ANALYTICS & TRACKING =====
  initAnalytics() {
    // Track CTA button clicks
    const ctaButtons = document.querySelectorAll('.button--primary, .bundle-card__cta');
    ctaButtons.forEach(button => {
      button.addEventListener('click', () => {
        const buttonText = button.textContent.trim();
        this.trackEvent('CTA', 'Click', buttonText);
      });
    });

    // Track FAQ interactions
    const faqToggles = document.querySelectorAll('[data-faq-toggle]');
    faqToggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        const question = toggle.querySelector('.faq-item__question-text').textContent.trim();
        this.trackEvent('FAQ', 'Toggle', question);
      });
    });

    // Track scroll depth
    this.initScrollDepthTracking();
  }

  trackPageView() {
    this.trackEvent('Page', 'View', window.location.pathname);
  }

  trackEvent(category, action, label, value) {
    // Google Analytics 4
    if (typeof gtag !== 'undefined') {
      gtag('event', action, {
        event_category: category,
        event_label: label,
        value: value
      });
    }

    // Facebook Pixel
    if (typeof fbq !== 'undefined') {
      fbq('trackCustom', `${category}_${action}`, {
        label: label,
        value: value
      });
    }

    // Console log for debugging
    console.log('Event tracked:', { category, action, label, value });
  }

  initScrollDepthTracking() {
    let maxScroll = 0;
    const milestones = [25, 50, 75, 100];
    const trackedMilestones = new Set();

    window.addEventListener('scroll', () => {
      const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
      
      if (scrollPercent > maxScroll) {
        maxScroll = scrollPercent;
        
        milestones.forEach(milestone => {
          if (scrollPercent >= milestone && !trackedMilestones.has(milestone)) {
            trackedMilestones.add(milestone);
            this.trackEvent('Scroll', 'Depth', `${milestone}%`);
          }
        });
      }
    });
  }

  // ===== UTILITY METHODS =====
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    }
  }

  // ===== PERFORMANCE OPTIMIZATION =====
  preloadCriticalResources() {
    // Preload critical images
    const criticalImages = [
      '/assets/hero-product-image.jpg',
      '/assets/product-demo-thumbnail.jpg'
    ];

    criticalImages.forEach(src => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = src;
      document.head.appendChild(link);
    });
  }

  // ===== ERROR HANDLING =====
  handleError(error, context = 'Unknown') {
    console.error(`Theme Error (${context}):`, error);
    
    // Track errors for debugging
    this.trackEvent('Error', 'JavaScript', `${context}: ${error.message}`);
  }
}

// ===== CART FUNCTIONALITY =====
class Cart {
  constructor() {
    this.items = [];
    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    // Add to cart buttons
    document.addEventListener('click', (e) => {
      if (e.target.matches('.add-to-cart, .bundle-card__cta')) {
        e.preventDefault();
        this.handleAddToCart(e.target);
      }
    });
  }

  async handleAddToCart(button) {
    const productData = this.getProductDataFromButton(button);
    
    try {
      button.disabled = true;
      button.textContent = 'Adding...';
      
      await this.addToCart(productData);
      
      // Show success feedback
      this.showAddToCartSuccess(button);
      
      // Track conversion
      if (typeof theme !== 'undefined') {
        theme.trackEvent('Ecommerce', 'Add to Cart', productData.title, productData.price);
      }
      
    } catch (error) {
      this.showAddToCartError(button);
      console.error('Add to cart error:', error);
    } finally {
      setTimeout(() => {
        button.disabled = false;
        button.textContent = productData.originalText;
      }, 2000);
    }
  }

  getProductDataFromButton(button) {
    const bundleCard = button.closest('.bundle-card');
    const bundleType = button.getAttribute('onclick')?.match(/addToCart\('(.+?)'\)/)?.[1] || 'single';
    
    return {
      id: bundleType,
      title: bundleCard?.querySelector('.bundle-card__title')?.textContent || 'Portable Arm Trainer',
      price: bundleCard?.querySelector('.bundle-card__price-current')?.textContent || '$29.99',
      quantity: bundleType === 'bundle2' ? 2 : bundleType === 'bundle3' ? 3 : 1,
      originalText: button.textContent
    };
  }

  async addToCart(productData) {
    // In a real implementation, this would make an API call to Shopify's Cart API
    // For demo purposes, we'll simulate the API call
    return new Promise((resolve) => {
      setTimeout(() => {
        this.items.push(productData);
        resolve();
      }, 1000);
    });
  }

  showAddToCartSuccess(button) {
    button.textContent = '✓ Added to Cart!';
    button.style.backgroundColor = 'var(--color-success)';
  }

  showAddToCartError(button) {
    button.textContent = 'Error - Try Again';
    button.style.backgroundColor = 'var(--color-error)';
  }
}

// ===== INITIALIZE THEME =====
const theme = new Theme();
const cart = new Cart();

// ===== EXPOSE GLOBAL FUNCTIONS =====
window.addToCart = function(bundleType) {
  const button = event.target;
  cart.handleAddToCart(button);
};

// ===== SERVICE WORKER REGISTRATION =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration);
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// ===== EXPORT FOR MODULE USAGE =====
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Theme, Cart };
}