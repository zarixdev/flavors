# Dzisiejsze Smaki Lodów

## What This Is

A web application for a single ice cream shop that displays currently available flavors. The public frontend shows today's selection with photos and tags (vegan, lactose-free, hit of the day). The admin panel allows the owner to quickly update (30-60 seconds) the daily flavor selection from a central flavor database. The goal is to inform customers before they visit and drive physical traffic to the shop.

## Core Value

Daily updates are fast enough (30-60 seconds) that the owner actually uses the system every day, keeping customers accurately informed about what's available right now.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Frontend - Public Display:**
- [ ] Mobile-first responsive design
- [ ] Display today's available flavors as photo cards (grid 2-3 columns)
- [ ] Each flavor card shows: photo, name, optional description, tags (vegan, lactose-free, new, hit of the day)
- [ ] Display last update timestamp
- [ ] Show availability disclaimer: "Flavors may change during the day - ask staff for current availability"
- [ ] Promotional section: craft production, fresh ingredients, seasonal flavors
- [ ] Location section: Google Maps embed, opening hours, CTA button
- [ ] Very fast loading with optimized images
- [ ] SEO-friendly (indexable content)

**Admin - Flavor Database:**
- [ ] Simple authentication (single owner account)
- [ ] Central flavor database with fields: name, slug (auto), description, type (milk/sorbet), tags, seasonal flag, photo, status (active/archived), created date
- [ ] Add new flavor form with required fields (name, photo) and optional fields
- [ ] Automatic image compression and cropping on upload
- [ ] Edit existing flavors
- [ ] Archive flavors (instead of deleting)
- [ ] Restore archived flavors
- [ ] Mobile-friendly admin interface

**Admin - Daily Flavor Management:**
- [ ] Separate "Today's Flavors" view showing all flavors from database
- [ ] Select which flavors are available today (checkboxes or toggle)
- [ ] Reorder today's flavors (drag & drop or up/down buttons)
- [ ] Mark specific flavor as "hit of the day"
- [ ] Quick actions: copy yesterday's selection, hide sold flavor, clear all
- [ ] Changes visible on public frontend immediately
- [ ] Update operation takes 30-60 seconds max

### Out of Scope

- **Online sales** — Physical shop only, no e-commerce
- **Inventory management** — No stock tracking, just visual availability
- **POS integration** — No point-of-sale system connection
- **Multi-tenant SaaS** — Single shop for MVP, potential future expansion
- **QR code generation** — Deferred to post-MVP
- **Flavor history** — No previous days archive in MVP
- **Social proof elements** — Deferred to post-MVP
- **Multiple admin users** — Owner only, no staff accounts
- **Real-time notifications** — No push notifications or alerts

## Context

**Current situation:**
- Single ice cream shop with no systematic online flavor communication
- Currently customers ask in-person or see nothing before visiting
- Owner wants to drive physical visits by showing what's available today

**User profile:**
- Admin: shop owner, single user, updates daily from mobile phone
- Public: customers checking flavors before visiting, mobile-first usage

**Photo workflow:**
- Mix of professional photos and phone camera uploads
- Varying quality requires robust auto-optimization
- Photos are primary content - visual appeal is critical

**Success metrics:**
- Owner updates the system daily (panel is simple enough for regular use)
- Customers check flavors before visiting (traffic on site, mentions in conversations)

## Constraints

- **Tech stack**: Django + HTMX + Tailwind CSS — No React, no Node.js, minimal JavaScript (HTMX only)
- **JavaScript policy**: Use HTMX for interactivity; custom JavaScript only if explicitly justified and approved
- **Database**: SQLite — Adequate for single shop, simpler deployment
- **Hosting**: Domain and hosting already available
- **Performance**: Very fast loading required — Photo optimization is critical
- **Mobile**: Mobile-first design for both public frontend and admin panel
- **SEO**: Content must be indexable by search engines
- **Deployment**: Must work on existing hosting environment

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Django + HTMX over React | Simpler stack, no build process, mobile-friendly admin, server-rendered for SEO | — Pending |
| SQLite over PostgreSQL | Single shop doesn't need PostgreSQL complexity; SQLite adequate for load | — Pending |
| Photo-centric design | Images are primary content; text descriptions secondary | — Pending |
| Single admin user | Owner only for MVP; no role management complexity | — Pending |
| No online sales | Focus on driving physical visits, not competing with delivery apps | — Pending |
| Separate flavor database from daily selection | Owner builds library over time, then quick-selects each day | — Pending |

---
*Last updated: 2026-01-30 after initialization*
