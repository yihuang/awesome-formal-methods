import { defineConfig } from 'vitepress'

// GitHub Pages project site: https://yihuang.github.io/awesome-formal-methods/
// If you rename the repo or move to a user/org site (yihuang.github.io),
// change `base` accordingly (''' for a root site).
const BASE = '/awesome-formal-methods/'

/**
 * GitHub-compatible heading slugifier.
 *
 * VitePress's default slugger prefixes headings that start with a digit with an
 * underscore (`## 1. Foo` -> `_1-foo`), which breaks every cross-page anchor
 * written in GitHub's style (`#1-foo`). Since this wiki is read both on GitHub
 * and as a generated site, we force ONE slug convention so the same anchor
 * works in both renderers.
 *
 * Mirrors tools/check-links.py and GitHub's `github-slugger`:
 * lowercase -> drop punctuation (keep letters/digits/_/-) -> each space to '-'.
 * Note: per-space replacement (not collapsing), so "Cedar — verified" yields a
 * double hyphen, exactly as GitHub does.
 */
function githubSlugify(str) {
  return String(str)
    .trim()
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s_-]/gu, '')
    .replace(/ /g, '-')
}

export default defineConfig({
  title: 'Formal Methods in the AI Era',
  description:
    'A talk-prep knowledge wiki introducing formal methods to engineers: ' +
    'fundamentals, history, industry applications, tooling, and the two-way ' +
    'relationship between AI and formal verification.',
  base: BASE,
  lang: 'en-US',
  cleanUrls: false,
  lastUpdated: true,
  ignoreDeadLinks: false,

  head: [
    ['meta', { name: 'theme-color', content: '#3451b2' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Formal Methods in the AI Era' }],
    [
      'meta',
      {
        property: 'og:description',
        content:
          'AI made code cheap. Trust is still expensive. A wiki on formal methods for engineers.'
      }
    ]
  ],

  markdown: {
    lineNumbers: false,
    theme: { light: 'github-light', dark: 'github-dark' },
    anchor: {
      slugify: githubSlugify
    }
  },

  themeConfig: {
    siteTitle: 'Formal Methods in the AI Era',

    nav: [
      { text: 'Why now', link: '/00-orientation/why-now' },
      {
        text: 'Learn',
        items: [
          { text: 'Orientation', link: '/00-orientation/why-now' },
          { text: 'Fundamentals', link: '/01-fundamentals/' },
          { text: 'History', link: '/02-history/' },
          { text: 'Applications', link: '/03-applications/' },
          { text: 'AI era', link: '/04-ai-era/' }
        ]
      },
      {
        text: 'Use it',
        items: [
          { text: 'Tool catalog', link: '/05-tools/catalog' },
          { text: 'Choosing a tool', link: '/05-tools/choosing' },
          { text: 'Adoption playbook', link: '/06-practice/adoption-playbook' },
          { text: 'Objections & answers', link: '/06-practice/objections' },
          { text: 'Demos', link: '/demos' },
          { text: 'Slide outline', link: '/slides/outline' }
        ]
      },
      {
        text: 'Reference',
        items: [
          { text: 'Glossary', link: '/references/glossary' },
          { text: 'Bibliography', link: '/references/bibliography' },
          { text: 'Quote bank', link: '/references/quote-bank' },
          { text: 'Research notes & confidence ledger', link: '/research-notes' },
          { text: 'Reading paths', link: '/00-orientation/reading-paths' }
        ]
      }
    ],

    sidebar: [
      {
        text: 'Start here',
        items: [
          { text: 'Wiki home', link: '/' },
          { text: 'Why now?', link: '/00-orientation/why-now' },
          { text: 'Taxonomy of the field', link: '/00-orientation/taxonomy' },
          { text: 'Reading paths', link: '/00-orientation/reading-paths' }
        ]
      },
      {
        text: '01 · Fundamentals',
        collapsed: false,
        items: [
          { text: 'Index', link: '/01-fundamentals/' },
          { text: 'Specifications', link: '/01-fundamentals/specifications' },
          { text: 'Logics', link: '/01-fundamentals/logics' },
          { text: 'Techniques', link: '/01-fundamentals/techniques' },
          { text: 'Automated reasoning', link: '/01-fundamentals/automated-reasoning' },
          { text: 'Limits', link: '/01-fundamentals/limits' }
        ]
      },
      {
        text: '02 · History',
        collapsed: false,
        items: [
          { text: 'Index', link: '/02-history/' },
          { text: 'Timeline (1666–2026)', link: '/02-history/timeline' },
          { text: 'The narrative arc', link: '/02-history/narrative' }
        ]
      },
      {
        text: '03 · Applications',
        collapsed: false,
        items: [
          { text: 'Index', link: '/03-applications/' },
          { text: 'Case studies', link: '/03-applications/case-studies' },
          { text: 'Distributed systems', link: '/03-applications/distributed-systems' },
          { text: 'Hardware & cryptography', link: '/03-applications/hardware-crypto' },
          { text: 'Safety-critical', link: '/03-applications/safety-critical' },
          { text: 'Lightweight FM (the on-ramp)', link: '/03-applications/lightweight-fm' },
          { text: 'The adoption gap', link: '/03-applications/adoption-gap' }
        ]
      },
      {
        text: '04 · AI era',
        collapsed: false,
        items: [
          { text: 'Index — the bidirectional map', link: '/04-ai-era/' },
          { text: 'AI → FM (accelerator)', link: '/04-ai-era/ai-for-fm' },
          { text: 'FM → AI (guardrails)', link: '/04-ai-era/fm-for-ai' },
          { text: 'The verification bottleneck', link: '/04-ai-era/verification-bottleneck' }
        ]
      },
      {
        text: '05 · Tools',
        collapsed: false,
        items: [
          { text: 'Index', link: '/05-tools/' },
          { text: 'Tool catalog', link: '/05-tools/catalog' },
          { text: 'Choosing a tool', link: '/05-tools/choosing' }
        ]
      },
      {
        text: '06 · Practice',
        collapsed: false,
        items: [
          { text: 'Index', link: '/06-practice/' },
          { text: 'Adoption playbook', link: '/06-practice/adoption-playbook' },
          { text: 'Objections & answers', link: '/06-practice/objections' }
        ]
      },
      {
        text: 'Do it',
        collapsed: false,
        items: [
          { text: 'Runnable demos', link: '/demos' },
          { text: 'Slide outline (30/45/60 min)', link: '/slides/outline' }
        ]
      },
      {
        text: 'Reference',
        collapsed: false,
        items: [
          { text: 'Glossary', link: '/references/glossary' },
          { text: 'Bibliography', link: '/references/bibliography' },
          { text: 'Quote bank', link: '/references/quote-bank' },
          { text: 'Research notes & confidence ledger', link: '/research-notes' }
        ]
      }
    ],

    search: {
      provider: 'local',
      options: {
        detailedView: true
      }
    },

    outline: { level: [2, 3], label: 'On this page' },

    editLink: {
      pattern: 'https://github.com/yihuang/awesome-formal-methods/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },

    docFooter: {
      prev: 'Previous',
      next: 'Next'
    },

    lastUpdated: {
      text: 'Last updated',
      formatOptions: { dateStyle: 'medium' }
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yihuang/awesome-formal-methods' }
    ],

    footer: {
      message:
        'Claims carry sources; uncertain numbers are flagged in the ' +
        '<a href="' +
        BASE +
        'research-notes.html">confidence ledger</a>. Corrections welcome.',
      copyright: 'Built as prep material for a tech-sharing talk.'
    },

    notFound: {
      title: 'Page not found',
      quote: 'A proof is a contract between your model and your property. It tells you nothing about either.',
      linkText: 'Back to the wiki home'
    },

    returnToTopLabel: 'Back to top',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Appearance',
    lightModeSwitchTitle: 'Switch to light theme',
    darkModeSwitchTitle: 'Switch to dark theme'
  }
})
