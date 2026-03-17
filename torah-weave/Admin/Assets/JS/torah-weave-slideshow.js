/**
 * TorahWeaveSlideshow - Reusable slideshow component
 * Version 1.0 - December 2025
 * 
 * Features:
 * - Fade transitions
 * - Adjacent slide preloading  
 * - Keyboard navigation
 * - Touch/swipe support
 * - Dot navigation
 * - Multiple slideshow support per page
 * 
 * Usage:
 *   new TorahWeaveSlideshow({
 *     container: '.slideshow-wrapper',
 *     totalSlides: 15,
 *     slideFolder: 'genesis-matrix-slides',
 *     slidePrefix: 'slide-',
 *     slideExtension: '.webp'
 *   });
 */

class TorahWeaveSlideshow {
    constructor(options) {
        // Get container element
        this.container = typeof options.container === 'string' 
            ? document.querySelector(options.container) 
            : options.container;
            
        if (!this.container) {
            console.warn('TorahWeaveSlideshow: Container not found');
            return;
        }
        
        // Configuration
        this.totalSlides = options.totalSlides || this.countSlides();
        this.slideFolder = options.slideFolder || '';
        this.slidePrefix = options.slidePrefix || 'slide-';
        this.slideExtension = options.slideExtension || '.webp';
        
        // ID suffix for multiple slideshows
        this.idSuffix = options.idSuffix || '';
        
        // State
        this.currentSlide = 1;
        this.touchStartX = 0;
        
        // Initialize
        this.init();
    }
    
    /**
     * Count slides if totalSlides not provided
     */
    countSlides() {
        return this.container.querySelectorAll('.slide').length;
    }
    
    /**
     * Initialize all event bindings
     */
    init() {
        this.cacheElements();
        this.bindButtons();
        this.bindDots();
        this.bindKeyboard();
        this.bindTouch();
        this.preloadAdjacent();
    }
    
    /**
     * Cache frequently accessed elements
     */
    cacheElements() {
        const suffix = this.idSuffix ? `-${this.idSuffix}` : '';
        this.prevBtn = document.getElementById(`prevSlide${suffix}`);
        this.nextBtn = document.getElementById(`nextSlide${suffix}`);
        this.counter = document.getElementById(`currentSlide${suffix}`);
        this.slides = this.container.querySelectorAll('.slide');
        this.dots = this.container.querySelectorAll('.slide-dot');
    }
    
    /**
     * Navigate to a specific slide
     */
    goToSlide(n) {
        if (n < 1 || n > this.totalSlides) return;
        
        // Update slides
        this.slides.forEach(slide => slide.classList.remove('active'));
        const newSlide = this.container.querySelector(`.slide[data-slide="${n}"]`);
        if (newSlide) newSlide.classList.add('active');
        
        // Update dots
        this.dots.forEach(dot => dot.classList.remove('active'));
        const newDot = this.container.querySelector(`.slide-dot[data-slide="${n}"]`);
        if (newDot) newDot.classList.add('active');
        
        // Update state
        this.currentSlide = n;
        
        // Update counter
        if (this.counter) this.counter.textContent = n;
        
        // Update button states
        if (this.prevBtn) this.prevBtn.disabled = (n === 1);
        if (this.nextBtn) this.nextBtn.disabled = (n === this.totalSlides);
        
        // Preload adjacent slides
        this.preloadAdjacent();
    }
    
    /**
     * Go to next slide
     */
    next() {
        if (this.currentSlide < this.totalSlides) {
            this.goToSlide(this.currentSlide + 1);
        }
    }
    
    /**
     * Go to previous slide
     */
    prev() {
        if (this.currentSlide > 1) {
            this.goToSlide(this.currentSlide - 1);
        }
    }
    
    /**
     * Preload adjacent slides for smooth transitions
     */
    preloadAdjacent() {
        if (this.currentSlide > 1) {
            this.preloadSlide(this.currentSlide - 1);
        }
        if (this.currentSlide < this.totalSlides) {
            this.preloadSlide(this.currentSlide + 1);
        }
    }
    
    /**
     * Preload a specific slide image
     */
    preloadSlide(n) {
        if (n >= 1 && n <= this.totalSlides && this.slideFolder) {
            const img = new Image();
            const paddedNum = String(n).padStart(2, '0');
            img.src = `${this.slideFolder}/${this.slidePrefix}${paddedNum}${this.slideExtension}`;
        }
    }
    
    /**
     * Bind prev/next button events
     */
    bindButtons() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
    }
    
    /**
     * Bind dot navigation events
     */
    bindDots() {
        this.dots.forEach(dot => {
            dot.addEventListener('click', () => {
                const slideNum = parseInt(dot.dataset.slide);
                if (!isNaN(slideNum)) {
                    this.goToSlide(slideNum);
                }
            });
        });
    }
    
    /**
     * Bind keyboard navigation
     */
    bindKeyboard() {
        // Store reference for cleanup
        this.keyHandler = (e) => {
            // Only handle if slideshow is visible
            if (!this.isInViewport()) return;
            
            if (e.key === 'ArrowLeft') {
                this.prev();
            } else if (e.key === 'ArrowRight') {
                this.next();
            }
        };
        
        document.addEventListener('keydown', this.keyHandler);
    }
    
    /**
     * Check if slideshow is in viewport (for keyboard nav)
     */
    isInViewport() {
        const rect = this.container.getBoundingClientRect();
        return (
            rect.top < window.innerHeight &&
            rect.bottom > 0
        );
    }
    
    /**
     * Bind touch/swipe events for mobile
     */
    bindTouch() {
        this.container.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
        }, { passive: true });
        
        this.container.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const diff = this.touchStartX - touchEndX;
            
            // Require minimum swipe distance of 50px
            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    this.next(); // Swipe left = next
                } else {
                    this.prev(); // Swipe right = prev
                }
            }
        }, { passive: true });
    }
    
    /**
     * Cleanup event listeners (call when removing slideshow)
     */
    destroy() {
        if (this.keyHandler) {
            document.removeEventListener('keydown', this.keyHandler);
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TorahWeaveSlideshow;
}