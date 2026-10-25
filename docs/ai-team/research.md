# Research log (Agent 1)

## 2026-10-25 (first run)
**Looked at**
- japan-guide.com, shinkansen page (https://www.japan-guide.com/e/e2018.html), checked 2026-10-25 via a summarising fetch tool.
  Good: breadcrumb, "on this page" contents near the top, question-style subheadings, related-page sub-navigation.
  Compared with us: we already have breadcrumb, contents box, short answer box (added 10-24) and related guides. Nothing new to copy this time.
- axe-core rule *scrollable-region-focusable* (https://dequeuniversity.com/rules/axe/4.10/scrollable-region-focusable), checked 2026-10-25.
  Scrollable areas must be reachable by keyboard (WCAG 2.1.1). Fix: `tabindex="0"` on the scrolling element.

**Applicable ideas** → keyboard-reachable wide tables (done); unique names for menus (done).
Later candidates: question-style subheadings are article content (out of our scope).

**Limits**: the fetch tool summarises pages with a small model, so its suggestions are hints, not facts.
No Lighthouse/real-device run this time.
