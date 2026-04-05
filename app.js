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
  card.innerHTML = `
    <div class="article-card-accent" style="background: ${article.accentColor};"></div>
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

// ===== HEADER COLLAPSE ON SCROLL =====
let lastScrollY = 0;
window.addEventListener('scroll', () => {
  const currentScrollY = window.scrollY;

  if (currentScrollY > 20) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }

  // Hide header on scroll down, show on scroll up
  if (currentScrollY > lastScrollY && currentScrollY > 100) {
    header.classList.add('hidden');
  } else {
    header.classList.remove('hidden');
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

  resetAndLoad();
});

// ===== INIT =====
initTheme();
ARTICLES = ARTICLES_DATA;
resetAndLoad();

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
