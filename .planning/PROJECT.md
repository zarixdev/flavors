# Dzisiejsze Smaki Lodów

## What This Is

A web application for a single ice cream shop that displays currently available flavors. The public frontend shows today's selection with photos and tags (vegan, lactose-free, hit of the day). The admin panel allows the owner to quickly update (30-60 seconds) the daily flavor selection from a central flavor database. The goal is to inform customers before they visit and drive physical traffic to the shop.

**Shipped:** v1.0 MVP (2026-02-01) — See [Milestone Archive](.planning/milestones/v1.0-ROADMAP.md)

## Core Value

Daily updates are fast enough (30-60 seconds) that the owner actually uses the system every day, keeping customers accurately informed about what's available right now.

**Validated:** ✅ Owner can update flavors in <60 seconds via mobile-optimized admin panel

---

## Current State (Post-v1.0)

**Version:** v1.0 MVP (shipped 2026-02-01)
**Stack:** Django 6.0.1 + HTMX + Tailwind CSS + SQLite (WAL mode)
**Codebase:** ~2,500 LOC across Python templates, CSS, JS
**Hosting:** Ready for production deployment (WhiteNoise, security headers configured)

### What's Working

- ✅ Full flavor CRUD with photo optimization (WebP, 1200px)
- ✅ Daily selection workflow (toggle, reorder, hit of day, copy from yesterday)
- ✅ Public homepage with responsive grid and SEO
- ✅ Mobile-optimized admin panel (44px touch targets)
- ✅ HTMX interactivity with loading states and error handling

### Next Milestone Ideas

- **v1.1 Performance** — Image CDN, caching, database query optimization
- **v1.2 Analytics** — Basic stats on flavor popularity, visitor tracking
- **v2.0 Multi-shop** — SaaS expansion for multiple ice cream shops

---

## Requirements

### Validated (v1.0 MVP)

**Frontend - Public Display:**
- ✅ Mobile-first responsive design
- ✅ Display today's available flavors as photo cards
- ✅ Flavor cards with photo, name, description, tags
- ✅ Display last update timestamp
- ✅ Show availability disclaimer
- ✅ Location section with hours
- ✅ Very fast loading with optimized images
- ✅ SEO-friendly (indexable content)

**Admin - Flavor Database:**
- ✅ Simple authentication (single owner account)
- ✅ Central flavor database with all fields
- ✅ Add new flavor form with required fields
- ✅ Automatic image compression on upload
- ✅ Edit existing flavors
- ✅ Archive flavors (soft delete)
- ✅ Restore archived flavors
- ✅ Mobile-friendly admin interface

**Admin - Daily Flavor Management:**
- ✅ Separate "Today's Flavors" view
- ✅ Select which flavors are available today
- ✅ Reorder today's flavors
- ✅ Mark specific flavor as "hit of the day"
- ✅ Quick actions: copy yesterday's selection
- ✅ Changes visible immediately on public frontend
- ✅ Update operation takes 30-60 seconds max

### Active (v1.1+ Candidates)

- [ ] Image CDN integration (Cloudflare, S3)
- [ ] Database query caching
- [ ] Analytics dashboard (flavor popularity, visits)
- [ ] Automated backup system
- [ ] Email notifications for low selection days

### Out of Scope (Validated Decisions)

- **Online sales** — ✅ Physical shop focus is correct
- **Inventory management** — ✅ Visual availability sufficient
- **POS integration** — ✅ Not needed for customer info site
- **Multi-tenant SaaS** — ✅ Single shop is right MVP scope
- **QR code generation** — ✅ Can be added later if needed
- **Flavor history/archive** — ✅ Not core value
- **Multiple admin users** — ✅ Owner-only keeps it simple
- **Real-time notifications** — ✅ Not needed

---

## Context

**Current situation:**
- v1.0 MVP is complete and ready for production
- Single ice cream shop with systematic online flavor communication
- Owner can update daily flavors in under 60 seconds from mobile phone

**User profile:**
- Admin: shop owner, updates daily from mobile phone
- Public: customers checking flavors before visiting, mobile-first usage

**Success metrics (v1.0):**
- ✅ Owner updates system daily (panel is simple enough)
- ⏳ Customers check before visiting (to be validated after launch)

---

## Constraints (Still Apply)

- **Tech stack**: Django + HTMX + Tailwind CSS
- **Database**: SQLite with WAL mode
- **Mobile-first**: Both public and admin interfaces
- **SEO**: Indexable content required
- **Performance**: Photo optimization critical

---

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Django + HTMX over React | Simpler stack, no build, mobile-friendly, SEO | ✅ Excellent — fast dev, smooth UX |
| SQLite over PostgreSQL | Single shop doesn't need complexity | ✅ Good — WAL mode works well |
| Photo-centric design | Images are primary content | ✅ Validated — visual appeal critical |
| Single admin user | Owner only for MVP | ✅ Right scope |
| No online sales | Drive physical visits | ✅ Correct focus |
| Separate flavor DB from daily selection | Build library, quick-select daily | ✅ Workflow validated |
| URL prefix /panel/ | Avoid Django Admin conflicts | ✅ Clean routing achieved |

---

*Last updated: 2026-02-01 after v1.0 MVP completion*
