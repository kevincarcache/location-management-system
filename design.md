# Design System Strategy: Atelier Estate - Editorial Hospitality & Place

This storefront should feel like an editorial guide to places, not a generic branch locator. The experience must stay discovery-first, warm, geographic, and premium while remaining grounded in Vuetify primitives for structure and interaction.

## 0. Implementation Constraint
- This frontend must be designed and implemented Vuetify-first.
- Prefer native Vuetify building blocks such as `v-app`, `v-container`, `v-row`, `v-col`, `v-sheet`, `v-toolbar`, `v-navigation-drawer`, `v-list`, `v-btn`, `v-chip`, `v-text-field`, `v-alert`, and `v-footer`.
- Do not redesign the UI around utility-class frameworks or custom layout systems.
- For this implementation pass, avoid custom CSS files and avoid custom classes unless a third-party integration makes them unavoidable.
- Prefer Vuetify theme tokens, props, variants, density, spacing utilities, typography utilities, borders, and layout primitives before introducing any custom styling.
- The result should feel bespoke, but the component foundation should remain recognizably Vuetify.

## 1. Vision & Personality
- Core essence: editorial, warm, premium, curated.
- Brand voice: the digital curator of destinations and service points.
- User experience: discovery-oriented, map-led, calm, and spatially aware.
- Product promise: help people understand where to go, what they will find there, and why each place matters.

## 2. Visual Thesis
- Mood: coastal architecture, hospitality print design, paper textures, and quiet luxury.
- Atmosphere: luminous and layered rather than stark white or dark-mode heavy.
- Composition: wide canvases, narrow text columns, strong map presence, and deliberate whitespace.
- Avoid: SaaS dashboards, card grids as the main expression, loud gradients, heavy borders, or over-decorated chrome.

## 3. Visual Language

### Color Palette: Natural Elements
- Deep Teal `#2D5A61`: primary anchor for headlines, active map states, and important actions.
- Stone and Sand neutrals: foundational backgrounds with a paper-like warmth.
- Clay and Terracotta accents: secondary emphasis, active list states, and highlighted markers.
- Mist overlays: translucent panels with blur to create depth without heavy visual weight.

### Typography
- Headlines: `Newsreader` or another high-contrast serif with editorial presence.
- UI and body copy: `Inter` for legibility and clean operational detail.
- Styling: uppercase micro-labels with generous tracking for metadata, location taxonomy, and supporting labels.

### Surfaces
- Primary sections should use tonal separation and subtle borders instead of thick cards.
- Floating panels over the map can use backdrop blur, very soft shadows, and warm translucent fills.
- Roundness should be medium and refined, not pill-heavy or overly soft.

## 4. Core Components

### Top Navigation: The Lightbar
- Fixed-feeling but visually light, with translucent surfaces and blur.
- Brand displayed in two lines to feel more like a publication masthead than a product logo lockup.
- Desktop nav stays minimal.
- Mobile opens a large, elegant drawer with clear hierarchy and spacious taps.

### Hero: The Editorial Discovery Panel
- Split layout with emotional narrative on the left and functional search on the right.
- Left side carries the strongest typography on the page.
- Right side presents a search panel that feels integrated into the atmosphere, not dropped in as a utility widget.
- Include a small amount of operational context:
  - current storeview or context
  - number of locations
  - highlighted or featured places

### Location Workspace
- This is the main product surface and should dominate the composition.
- Left rail acts as a registry of places:
  - each row should show city, type, title, and a short line of context
  - active state should feel curated and warm, not merely selected
- Right side is the map canvas:
  - the map is the orientation anchor
  - markers should feel custom and premium
  - the summary overlay should present the selected location as if it were an editorial detail card

### Footer
- Keep it quiet, atmospheric, and useful.
- Reinforce brand, current context, and simple orientation links.
- It should feel like the closing note of an editorial page, not a legal dump.

## 5. Design Principles
1. Build custom expression on top of Vuetify primitives, not instead of them.
2. The map and location registry are the core experience, not supporting widgets.
3. Every location should feel distinct even when rendered in a compact list.
4. Whitespace is a product feature because it helps orientation.
5. Selection in the list must immediately and elegantly reflect on the map.
6. Prefer two typefaces maximum and one accent family.
7. Use motion sparingly but intentionally for entrance, hover, and emphasis.

## 6. Responsive Strategy
- Desktop: broad editorial canvas with sidebar and map side-by-side.
- Tablet: preserve the dual-surface feeling but tighten spacing and shorten text lines.
- Mobile: keep the map as the anchor and allow the list/navigation to stack or slide without losing orientation.
- Search, navigation, and selected-place details must remain obvious and tap-friendly on smaller screens.

## 7. Implementation Notes for AI
- Keep the data orchestration pattern intact in `useStorefrontPage.ts`.
- Express the visual system through Vuetify composition, theme, props, and utilities first.
- Do not add a parallel fetch pattern or a second route-state owner.
- Prefer atmospheric hierarchy, typography, chips, lists, and overlays over introducing many new structural abstractions.
