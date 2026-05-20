/* ============================================
   THE UNCONSCIOUS CONSUMER — App JS
   Infinite scroll, filtering, dark mode, nav
   ============================================ */

// ===== ARTICLE DATA (loaded from articles.json) =====
let ARTICLES = [];

// ===== STATE =====
let currentFilter = 'all';
let displayedCount = 0;
const BATCH_SIZE = 6;
let isLoading = false;
let allLoaded = false;
let searchQuery = '';

// ===== DOM REFS =====
const grid = document.getElementById('articles-grid');
const loader = document.getElementById('loader');
const noMoreMsg = document.getElementById('no-more-msg');
const loadMoreZone = document.getElementById('load-more-zone');
const themeToggle = document.getElementById('theme-toggle');
const header = document.getElementById('site-header');
const discoveryBar = document.getElementById('discovery-bar');
const discoveryPills = document.querySelectorAll('.discovery-pill:not(.discovery-search-toggle)');
const discoverySearchToggle = document.getElementById('discovery-search-toggle');
const discoverySearchWrapper = document.getElementById('discovery-search-wrapper');
const discoverySearchInput = document.getElementById('discovery-search-input');
const filterBtns = document.querySelectorAll('.filter-btn');
const navLinks = document.querySelectorAll('.nav-link[data-filter]');
const categoryHero = document.getElementById('category-hero');
const categoryHeroLabel = document.getElementById('category-hero-label');

// ===== CATEGORY LABELS =====
const HERO_LABELS = {
  'consumer-psychology': 'Consumer Psychology',
  'behavioural-economics': 'Behavioural Economics',
  'user-experience': 'User Experience',
  'undercurrents': 'Undercurrents'
};

// ===== CATEGORY HERO =====
function updateCategoryHero() {
  if (!categoryHero || !categoryHeroLabel) return;
  if (currentFilter === 'all' || searchQuery) {
    categoryHero.classList.add('hidden');
    categoryHeroLabel.classList.add('hidden');
    categoryHero.innerHTML = '';
    return;
  }
  categoryHeroLabel.textContent = HERO_LABELS[currentFilter] || currentFilter;
  categoryHeroLabel.classList.remove('hidden');
  categoryHero.classList.remove('hidden');
  var coverHtml = typeof generateCover === 'function' ? generateCover(currentFilter, true, '', 'cart') : '';
  categoryHero.innerHTML = coverHtml;
  // Execute animation scripts
  var scripts = categoryHero.querySelectorAll('script');
  scripts.forEach(function(s) {
    var newScript = document.createElement('script');
    newScript.textContent = s.textContent;
    document.body.appendChild(newScript);
  });
}

// ===== ARTICLE LINK HELPERS =====
function articleHref(article) {
  if (article.substackUrl) return article.substackUrl;
  return 'article.html?slug=' + article.slug;
}

function articleTarget(article) {
  return article.substackUrl ? 'target="_blank" rel="noopener"' : '';
}

// ===== HELPERS =====
function getCategoryTag(cat) {
  const map = {
    'consumer-psychology': { cls: 'tag-cp', label: 'Consumer Psychology' },
    'behavioural-economics': { cls: 'tag-be', label: 'Behavioural Economics' },
    'user-experience': { cls: 'tag-ux', label: 'User Experience' },
    'undercurrents': { cls: 'tag-uc', label: 'Undercurrents' },
  };
  return map[cat] || { cls: 'tag-cp', label: cat };
}

function getFilteredArticles() {
  let filtered = ARTICLES;

  // Apply search filter if active
  if (searchQuery.trim()) {
    filtered = filtered.filter(a =>
      a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
    );
  } else if (currentFilter !== 'all') {
    // Apply category filter only if not searching
    filtered = filtered.filter(a => a.category === currentFilter);
  }

  return filtered;
}

function createArticleCard(article) {
  const tag = getCategoryTag(article.category);
  const card = document.createElement('article');
  card.className = 'article-card';
  card.dataset.category = article.category;
  var coverHtml = article.coverImage
    ? `<img src="${article.coverImage}" alt="${article.title}" class="article-card-cover-img" loading="lazy">`
    : (typeof generateCover === 'function' ? generateCover(article.category, false, article.slug, article.coverObject) : '');
  card.innerHTML = `
    <div class="article-card-cover${article.coverImage ? ' article-card-cover--photo' : ''}">${coverHtml}</div>
    <div class="article-card-body">
      <span class="card-tag ${tag.cls}">${tag.label}</span>
      <h3 class="article-card-title">${article.title}</h3>
      <p class="article-card-excerpt">${article.excerpt}</p>
      <div class="article-card-meta">
        <span class="article-card-date">${article.date} · ${article.readTime}</span>
        <a href="${articleHref(article)}" ${articleTarget(article)} class="article-card-link">Read →</a>
      </div>
    </div>
  `;
  return card;
}

// ===== INFINITE SCROLL LOGIC =====
function loadMoreArticles() {
  if (isLoading || allLoaded) return;

  const filtered = getFilteredArticles();
  const remaining = filtered.slice(displayedCount, displayedCount + BATCH_SIZE);

  if (remaining.length === 0) {
    allLoaded = true;
    loader.classList.add('hidden');
    noMoreMsg.style.display = 'block';
    return;
  }

  isLoading = true;
  loader.classList.remove('hidden');

  // Simulate async loading (as if fetching from API)
  setTimeout(() => {
    const fragment = document.createDocumentFragment();
    remaining.forEach((article, i) => {
      const card = createArticleCard(article);
      card.style.animationDelay = `${i * 60}ms`;
      fragment.appendChild(card);
    });
    grid.appendChild(fragment);
    displayedCount += remaining.length;

    if (displayedCount >= filtered.length) {
      allLoaded = true;
      loader.classList.add('hidden');
      noMoreMsg.style.display = 'block';
    } else {
      loader.classList.add('hidden');
    }

    isLoading = false;
  }, 500);
}

function resetAndLoad() {
  grid.innerHTML = '';
  displayedCount = 0;
  allLoaded = false;
  isLoading = false;
  noMoreMsg.style.display = 'none';
  loader.classList.remove('hidden');
  loadMoreArticles();
}

// ===== INTERSECTION OBSERVER for INFINITE SCROLL =====
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !isLoading && !allLoaded) {
      loadMoreArticles();
    }
  });
}, { rootMargin: '200px' });

observer.observe(loadMoreZone);

// ===== FILTER BUTTONS =====
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.dataset.filter;
    if (filter === currentFilter) return;

    currentFilter = filter;
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Update discovery pills
    discoveryPills.forEach(p => {
      p.classList.toggle('active', p.dataset.filter === filter);
    });

    // Close search if open
    if (discoverySearchWrapper.classList.contains('active')) {
      discoverySearchWrapper.classList.remove('active');
      discoverySearchInput.value = '';
    }

    updateCategoryHero();
    resetAndLoad();
  });
});

// Nav links with data-filter
navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const filter = link.dataset.filter;
    currentFilter = filter;

    filterBtns.forEach(b => {
      b.classList.toggle('active', b.dataset.filter === filter);
    });

    document.getElementById('articles').scrollIntoView({ behavior: 'smooth' });
    updateCategoryHero();
    resetAndLoad();

    // Close mobile nav
    document.body.classList.remove('mobile-nav-open');
  });
});

// ===== DARK MODE =====
function initTheme() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
}

themeToggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// ===== HEADER SHRINK ON SCROLL =====
let lastScrollY = 0;
window.addEventListener('scroll', () => {
  const currentScrollY = window.scrollY;

  if (currentScrollY > 20) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }

  // Shrink header on scroll down, expand on scroll up
  if (currentScrollY > lastScrollY && currentScrollY > 100) {
    header.classList.add('shrink');
  } else {
    header.classList.remove('shrink');
  }

  lastScrollY = currentScrollY;
}, { passive: true });

// ===== DISCOVERY BAR PILLS =====
discoveryPills.forEach(pill => {
  pill.addEventListener('click', () => {
    const filter = pill.dataset.filter;
    if (filter === currentFilter) return;

    currentFilter = filter;
    discoveryPills.forEach(p => p.classList.remove('active'));
    pill.classList.add('active');

    // Update old filter buttons too
    filterBtns.forEach(b => {
      b.classList.toggle('active', b.dataset.filter === filter);
    });

    updateCategoryHero();
    resetAndLoad();
    document.getElementById('articles').scrollIntoView({ behavior: 'smooth' });
  });
});

// ===== DISCOVERY SEARCH =====
discoverySearchToggle.addEventListener('click', () => {
  discoverySearchWrapper.classList.toggle('active');
  if (discoverySearchWrapper.classList.contains('active')) {
    discoverySearchInput.focus();
  } else {
    // Clear search and reset to all articles
    discoverySearchInput.value = '';
    searchQuery = '';
    discoveryPills.forEach(p => p.classList.remove('disabled'));
    resetAndLoad();
  }
});

discoverySearchInput.addEventListener('input', (e) => {
  searchQuery = e.target.value.trim();

  // Don't change currentFilter when searching - just update the query
  // But disable category pills while searching
  discoveryPills.forEach(p => {
    p.classList.toggle('disabled', searchQuery.trim() !== '');
  });

  updateCategoryHero();
  resetAndLoad();
});

// ===== FEATURED HERO =====

// SELECTION METHOD: currently random from curated featured set.
// Future: replace the body of this function with engagement-based
// social proof logic. Nothing else needs to change.
function getFeaturedArticle(articles) {
  var featured = articles.filter(function(a) { return a.featured === true && a.coverImage; });
  if (featured.length > 0) {
    return featured[Math.floor(Math.random() * featured.length)];
  }
  // Fallback: most recent article that has a coverImage
  var withImage = articles.filter(function(a) { return a.coverImage; });
  return withImage.length
    ? withImage.slice().sort(function(a, b) { return new Date(b.date) - new Date(a.date); })[0]
    : null;
}

function renderFeaturedHero(article) {
  var bgLayer = document.getElementById('hero-bg-layer');
  var featuredLinkEl = document.getElementById('hero-featured-link');
  if (!bgLayer || !article) return;

  var VW = 1200, VH = 560;
  var imgW = 480, imgH = 480;
  var imgX = VW - imgW - 40;
  var imgY = Math.round((VH - imgH) / 2);

  bgLayer.innerHTML =
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"' +
    ' viewBox="0 0 ' + VW + ' ' + VH + '" preserveAspectRatio="xMaxYMid slice"' +
    ' style="width:100%;height:100%;display:block;">' +
    '<defs>' +
    '<filter id="hero-blur"><feGaussianBlur stdDeviation="6"/></filter>' +
    '<clipPath id="hero-clip-L"><rect id="hero-rect-L" x="0" y="0" width="600" height="' + VH + '"/></clipPath>' +
    '<clipPath id="hero-clip-R"><rect id="hero-rect-R" x="600" y="0" width="' + VW + '" height="' + VH + '"/></clipPath>' +
    '</defs>' +
    '<g clip-path="url(#hero-clip-L)" filter="url(#hero-blur)">' +
    '<image href="' + article.coverImage + '" x="' + imgX + '" y="' + imgY + '" width="' + imgW + '" height="' + imgH + '" preserveAspectRatio="xMidYMid meet"/>' +
    '</g>' +
    '<g clip-path="url(#hero-clip-R)">' +
    '<image href="' + article.coverImage + '" x="' + imgX + '" y="' + imgY + '" width="' + imgW + '" height="' + imgH + '" preserveAspectRatio="xMidYMid meet"/>' +
    '</g>' +
    '<rect id="hero-tint" x="0" y="0" width="600" height="' + VH + '" fill="rgba(15,11,9,0.09)"/>' +
    '<line id="hero-lens-line" x1="600" y1="0" x2="600" y2="' + VH + '" stroke="#C4531A" stroke-width="1" opacity="0.5"/>' +
    '</svg>';

  var rectL    = document.getElementById('hero-rect-L');
  var rectR    = document.getElementById('hero-rect-R');
  var lensLine = document.getElementById('hero-lens-line');
  var tint     = document.getElementById('hero-tint');

  var phase    = Math.random() * Math.PI * 2;
  var phaseInc = (2 * Math.PI) / (16 * 60);
  var minPct   = 0.20, maxPct = 0.72;

  (function tick() {
    phase += phaseInc;
    var lensX = Math.round(VW * (minPct + (maxPct - minPct) * (0.5 + 0.5 * Math.sin(phase))));
    rectL.setAttribute('width', lensX);
    rectR.setAttribute('x', lensX);
    rectR.setAttribute('width', VW - lensX);
    lensLine.setAttribute('x1', lensX);
    lensLine.setAttribute('x2', lensX);
    tint.setAttribute('width', lensX);
    requestAnimationFrame(tick);
  })();

  if (featuredLinkEl) {
    var href   = article.substackUrl || ('article.html?slug=' + article.slug);
    var target = article.substackUrl ? ' target="_blank" rel="noopener"' : '';
    featuredLinkEl.innerHTML =
      'Featured: <a href="' + href + '"' + target + '>' +
      article.title + ' <span class="featured-arrow">→</span></a>';
  }
}

// ===== INIT =====
initTheme();

fetch('articles.json')
  .then(function(r) { return r.json(); })
  .then(function(data) {
    ARTICLES = data;

    renderFeaturedHero(getFeaturedArticle(data));

    // Apply ?filter= URL param if present (e.g. coming from an article page category pill)
    var filterParam = new URLSearchParams(window.location.search).get('filter');
    if (filterParam && filterParam !== 'all') {
      currentFilter = filterParam;
      discoveryPills.forEach(function(p) {
        p.classList.toggle('active', p.dataset.filter === filterParam);
      });
      filterBtns.forEach(function(b) {
        b.classList.toggle('active', b.dataset.filter === filterParam);
      });
    }

    updateCategoryHero();
    resetAndLoad();
  })
  .catch(function() {
    grid.innerHTML = '<p style="padding: 2rem; color: var(--text-2);">Could not load articles. Please refresh the page.</p>';
    if (loader) loader.classList.add('hidden');
  });

// Highlight active nav on scroll
const sections = ['articles', 'about', 'reading'];
const scrollSpy = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      document.querySelectorAll('.nav-link:not([data-filter])').forEach(link => {
        const href = link.getAttribute('href');
        link.classList.toggle('active', href === `#${entry.target.id}`);
      });
    }
  });
}, { threshold: 0.3 });

sections.forEach(id => {
  const el = document.getElementById(id);
  if (el) scrollSpy.observe(el);
});
