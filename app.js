/* ============================================
   THE UNCONSCIOUS CONSUMER — App JS
   Infinite scroll, filtering, dark mode, nav
   ============================================ */

// ===== ARTICLE DATA =====
const ARTICLES = [
  // Consumer Psychology
  {
    id: 1,
    title: "From Page to Practice: Wearing Our Genes on Our Sleeves with 'Spent'",
    excerpt: "Geoffrey Miller's evolutionary lens on modern shopping reveals how ancient biological signals quietly guide our purchasing decisions — from luxury brands to fitness signals.",
    category: "consumer-psychology",
    date: "Feb 12, 2024",
    readTime: "8 min read",
    accentColor: "#2d6a9f",
    emoji: "🧬"
  },
  {
    id: 2,
    title: "Is This Legit? The Rise of the Skeptical Shopper",
    excerpt: "Five major forces are driving consumer skepticism to an all-time high — from rampant misinformation to growing demands for ethical business practices.",
    category: "consumer-psychology",
    date: "Aug 12, 2023",
    readTime: "6 min read",
    accentColor: "#2d6a9f",
    emoji: "🔍"
  },
  {
    id: 3,
    title: "Less is More: Unpacking the Power of Scarcity Bias",
    excerpt: "Scarcity bias operates below conscious awareness — shaping desire, urgency, and value perception. Here's how marketers exploit it and what that means ethically.",
    category: "consumer-psychology",
    date: "Aug 4, 2023",
    readTime: "7 min read",
    accentColor: "#2d6a9f",
    emoji: "⏳"
  },
  {
    id: 4,
    title: "The Endowment Effect: Why We Overvalue What We Own",
    excerpt: "Once something belongs to us, it becomes worth more — at least in our minds. Exploring the endowment effect and its implications for pricing, returns, and loyalty.",
    category: "consumer-psychology",
    date: "Jul 10, 2023",
    readTime: "5 min read",
    accentColor: "#2d6a9f",
    emoji: "🏷️"
  },
  // Behavioural Economics
  {
    id: 5,
    title: "From Page to Practice: The Power and Pitfalls of Applying Nudge Theory for Climate Action",
    excerpt: "Nudge theory promises to change behaviour without changing minds. But when applied to climate action, the stakes are higher and the limitations more glaring.",
    category: "behavioural-economics",
    date: "Jul 26, 2023",
    readTime: "9 min read",
    accentColor: "#4a7c2f",
    emoji: "🌍"
  },
  {
    id: 6,
    title: "From Page to Practice: Behaving 'Predictably Irrational' in an Unpredictable Economy",
    excerpt: "Dan Ariely's framework still holds — but how does predictable irrationality play out when the economic context itself is chaotic? A revisit with fresh eyes.",
    category: "behavioural-economics",
    date: "Jul 5, 2023",
    readTime: "8 min read",
    accentColor: "#4a7c2f",
    emoji: "📉"
  },
  {
    id: 7,
    title: "From Page to Practice: Applying 'Thinking, Fast and Slow' to Consumer Behaviour",
    excerpt: "Kahneman's dual-process theory is the bedrock of behavioural economics. Here's how System 1 and System 2 thinking shape every purchase decision you've ever made.",
    category: "behavioural-economics",
    date: "Jun 15, 2023",
    readTime: "10 min read",
    accentColor: "#4a7c2f",
    emoji: "🧠"
  },
  {
    id: 8,
    title: "Loss Aversion and the Psychology of Pricing",
    excerpt: "We feel losses roughly twice as intensely as equivalent gains. Marketers know this — and the way products are priced, framed, and discounted is a direct result.",
    category: "behavioural-economics",
    date: "May 22, 2023",
    readTime: "6 min read",
    accentColor: "#4a7c2f",
    emoji: "💸"
  },
  // User Experience
  {
    id: 9,
    title: "Play to Learn: Gamifying SaaS Onboarding",
    excerpt: "Gamification isn't just about points and badges. The most effective SaaS onboarding experiences borrow from game design to build habit, competence, and genuine delight.",
    category: "user-experience",
    date: "Jun 30, 2023",
    readTime: "7 min read",
    accentColor: "#6b35a0",
    emoji: "🎮"
  },
  {
    id: 10,
    title: "Game On or Game Over? The Ethical Crossroads of Gamification",
    excerpt: "The same design principles that drive engagement can also exploit vulnerabilities. Where is the line between motivating users and manipulating them?",
    category: "user-experience",
    date: "Jun 10, 2023",
    readTime: "8 min read",
    accentColor: "#6b35a0",
    emoji: "⚖️"
  },
  {
    id: 11,
    title: "Behind Dark Patterns: Unpacking Digital Deceptions",
    excerpt: "Sneaky opt-ins, roach motels, confirmshaming — dark patterns in UX are everywhere. A deep dive into the design decisions that manipulate users against their own interests.",
    category: "user-experience",
    date: "May 15, 2023",
    readTime: "9 min read",
    accentColor: "#6b35a0",
    emoji: "🌑"
  },
  {
    id: 12,
    title: "The Default Effect: How Pre-selected Options Shape Mass Behaviour",
    excerpt: "Most people never change defaults — whether it's organ donation, retirement savings, or app privacy settings. Understanding why is crucial for ethical product design.",
    category: "user-experience",
    date: "Apr 28, 2023",
    readTime: "6 min read",
    accentColor: "#6b35a0",
    emoji: "⚙️"
  },
  // Undercurrents
  {
    id: 13,
    title: "Undercurrents: How ChatGPT's Hypergrowth Rewired Consumer Expectations",
    excerpt: "ChatGPT's adoption rate shattered every previous benchmark. Beyond the numbers, what does this say about how consumers now think about speed, intelligence, and trust in AI?",
    category: "undercurrents",
    date: "Mar 5, 2023",
    readTime: "5 min read",
    accentColor: "#7a4a1a",
    emoji: "🤖"
  },
  {
    id: 14,
    title: "Undercurrents: Tesla's Range Controversy and the Fragility of Brand Trust",
    excerpt: "When a trusted brand is caught overstating a core product benefit, the psychological fallout is disproportionate. A look at Tesla's trust crisis through a behavioural lens.",
    category: "undercurrents",
    date: "Feb 20, 2023",
    readTime: "5 min read",
    accentColor: "#7a4a1a",
    emoji: "⚡"
  },
  {
    id: 15,
    title: "Undercurrents: AI-Driven Experiences and the Uncanny Valley of Personalization",
    excerpt: "There's a point where AI personalisation stops feeling helpful and starts feeling invasive. Mapping the new psychology of relevance, privacy, and algorithmic unease.",
    category: "undercurrents",
    date: "Jan 30, 2023",
    readTime: "6 min read",
    accentColor: "#7a4a1a",
    emoji: "🎯"
  },
  {
    id: 16,
    title: "Undercurrents: The Quiet Return of Analog in a Digital World",
    excerpt: "Vinyl records, paper notebooks, physical books — in a world of infinite digital convenience, why are analog experiences surging? The psychology of tactile resistance.",
    category: "undercurrents",
    date: "Jan 10, 2023",
    readTime: "5 min read",
    accentColor: "#7a4a1a",
    emoji: "📻"
  },
  {
    id: 17,
    title: "Social Proof in the Age of Fake Reviews",
    excerpt: "We rely on others' opinions to navigate uncertainty — but when reviews can be purchased and ratings gamed, what happens to the psychology of social proof?",
    category: "consumer-psychology",
    date: "Dec 12, 2022",
    readTime: "7 min read",
    accentColor: "#2d6a9f",
    emoji: "⭐"
  },
  {
    id: 18,
    title: "Anchoring Bias and the First Number You See",
    excerpt: "The first price, rating, or number you encounter becomes a mental anchor that colours every subsequent judgment. How anchoring shapes everything from salary negotiations to wine selection.",
    category: "behavioural-economics",
    date: "Nov 28, 2022",
    readTime: "6 min read",
    accentColor: "#4a7c2f",
    emoji: "⚓"
  }
];

// ===== STATE =====
let currentFilter = 'all';
let displayedCount = 0;
const BATCH_SIZE = 6;
let isLoading = false;
let allLoaded = false;

// ===== DOM REFS =====
const grid = document.getElementById('articles-grid');
const loader = document.getElementById('loader');
const noMoreMsg = document.getElementById('no-more-msg');
const loadMoreZone = document.getElementById('load-more-zone');
const themeToggle = document.getElementById('theme-toggle');
const menuToggle = document.getElementById('menu-toggle');
const header = document.getElementById('site-header');
const filterBtns = document.querySelectorAll('.filter-btn');
const navLinks = document.querySelectorAll('.nav-link[data-filter]');

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
  if (currentFilter === 'all') return ARTICLES;
  return ARTICLES.filter(a => a.category === currentFilter);
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
      <h3 class="article-card-title">${article.emoji} ${article.title}</h3>
      <p class="article-card-excerpt">${article.excerpt}</p>
      <div class="article-card-meta">
        <span class="article-card-date">${article.date} · ${article.readTime}</span>
        <a href="#" class="article-card-link">Read →</a>
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

// ===== HEADER SCROLL EFFECT =====
window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
}, { passive: true });

// ===== MOBILE MENU =====
menuToggle.addEventListener('click', () => {
  document.body.classList.toggle('mobile-nav-open');
});

// Close mobile nav on outside click
document.addEventListener('click', (e) => {
  if (!header.contains(e.target)) {
    document.body.classList.remove('mobile-nav-open');
  }
});

// ===== INIT =====
initTheme();
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
