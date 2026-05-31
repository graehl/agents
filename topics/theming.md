# Theming

> A theme is a coherent set of presentation values — color, typography,
> elevation — swappable as design-token data without changing layout or
> behavior; "skin" is the purely cosmetic end of that range, while density
> is the boundary case that does change spacing and so must be verified as
> layout.

Topic: theming

Subtopic of [`ui-quality`](ui-quality.md), and the *last* of its three
concerns by design: **design it, verify it, then theme it.** Theming layers
cosmetic variants (dark mode, brand skins) on top of a layout that
[`functional-layout`](functional-layout.md) already made correct and
[`ui-verification`](ui-verification.md) already proved correct — and it must
not disturb either. Its entire discipline is one promise: *change how it
looks, never what it is or how it behaves.*

## Vocabulary

- **mode** — a paired *environmental* variant the user or OS selects:
  light/dark, high-contrast. Driven by `color-scheme` /
  `prefers-color-scheme` and, for forced colors, `forced-colors`.
- **theme** — a named, runtime-selectable value set, often one per brand.
- **skin** — the purely surface end of a theme: color, texture, imagery,
  with no structural or behavioral effect. A constrained kind of theme, not
  a separate mechanism.
- **density** — a compact-vs-comfortable spacing scale. The **boundary
  case**: density changes spacing → geometry, so it is *not* a pure skin
  and must be verified like a layout change (see the contract below).
- **design token** — a named design decision stored as data (a color,
  space, type, radius, or elevation value), consumed at runtime as a CSS
  custom property. The unit a theme swaps.

## Design tokens

Tokens turn design decisions into data so they can be swapped wholesale.
The useful structure is **three layers** (Nathan Curtis / EightShapes; Brad
Frost, *Atomic Design*):

1. **Primitive / global** — raw values named by what they *are*:
   `color-blue-500: #3b82f6`, `space-4: 16px`. A flat palette, no intent.
2. **Semantic / alias** — values named by *role*, referencing primitives:
   `color-action-primary → {color.blue.500}`, `color-text-default`,
   `space-inset-md`. **This is the layer a theme swaps** — dark mode and
   brand skins remap the semantic layer onto different primitives while
   every component keeps asking for the same role.
3. **Component** (optional) — scoped to one component, referencing
   semantic: `button-bg → {color.action.primary}`. Use only when a
   component needs to vary independently of its role.

The indirection is the point: components consume *roles*, never raw
values, so a theme is a remap of roles → primitives and nothing in the
component tree changes.

**Interchange format.** The W3C Design Tokens Format Module gives a
vendor-neutral JSON encoding — each token an object with `$value` and
`$type`, aliasing by `{group.token}` reference, and groups that share a
type — so tokens move between design tools and code.
<!-- unconfirmed: 2026-05-31 spec maturity/property names -->

**Runtime.** Tokens compile to CSS custom properties on a scope:

```css
:root            { --color-text: #1a1a1a; --color-bg: #ffffff; }
[data-theme=dark]{ --color-text: #f0f0f0; --color-bg: #121212; }
.card            { color: var(--color-text); background: var(--color-bg); }
```

Swapping the theme is reassigning the variables on a wrapper — the cascade
re-resolves and the geometry never moves, because only values changed. Pair
it with the `color-scheme` property so the browser themes form controls,
scrollbars, and the like to match.

## The contract: presentation-only ★

Theming changes token *values*, never structure or logic. That makes the
contract a **verifiable claim**, not a matter of taste:

- A theme / skin / mode swap produces **zero layout shift** and **zero
  behavior change**. It is checked as a [`ui-verification`](ui-verification.md)
  appearance pass: capture the screenshot matrix in each theme; the
  *geometry* must be identical and only colors/textures differ. Element
  boxes, focus order, and interaction outcomes are unchanged.
- **Density is the explicit exemption.** It is a *layout* variant, so a
  density change is not held to "zero layout shift" — it re-runs the full
  layout verification instead of the theme-swap check. Treating density as
  "just another skin" and waving it through is the classic theming bug.
- **Typography sits on the boundary.** The type *scale* (sizes, rhythm) is
  layout, owned by [`functional-layout`](functional-layout.md) — changing
  it changes geometry. The *typeface* (font-family, weights) can be a theme
  token, but only if the swap preserves metrics (or uses `@font-face`
  metric overrides) so line counts don't change; otherwise a font swap is a
  layout change in disguise, exactly like density.

## Modes that aren't optional: forced colors & contrast

- **`forced-colors: active`** (Windows High Contrast and similar): the OS
  replaces your palette with the user's own. Don't fight it — use the CSS
  `system-color` keywords (`Canvas`, `CanvasText`, `LinkText`,
  `ButtonText`, `Highlight`) so your UI maps onto their palette, and reach
  for `forced-color-adjust: none` *only* where color carries essential
  meaning the user must still see (a color picker, a status swatch).
- **`prefers-contrast: more`**: offer a higher-contrast token set for users
  who ask the OS for one; it composes with light/dark as another mode axis.
- **`prefers-color-scheme`**: respect the OS light/dark preference as the
  default mode, with an in-app override that persists.

These are accessibility obligations, not brand choices, so they outrank a
skin: a brand skin must still resolve to legible contrast under each.

## User and third-party skins: the sandbox

If users or third parties can supply skins, the presentation-only contract
has to be *enforced*, not trusted. A safe skin can set **token values
only** — never structure, selectors, or behavior:

- Accept a value map against a known **token allowlist**; reject unknown
  keys.
- **Type-validate** each value (a color token must parse as a color, a
  space token as a length) so a skin can't smuggle `expression()`,
  `url(javascript:…)`, or arbitrary CSS into a property.
- Never let a skin inject raw CSS, selectors, or scripts — only the
  pre-declared custom properties the design system exposes.

This keeps "a skin changes only appearance" true even when the skin author
is untrusted, and keeps the [verification](ui-verification.md) claim (no
layout shift, no behavior change) meaningful.

## Sources

- W3C / Design Tokens Community Group — Design Tokens Format Module
  (designtokens.org).
- Nathan Curtis (EightShapes) — token taxonomy / naming layers; Brad Frost,
  *Atomic Design* — design-system structure.
- MDN — CSS custom properties, `color-scheme`, `prefers-color-scheme`,
  `forced-colors` / `forced-color-adjust`, `system-color` keywords,
  `prefers-contrast`; `@font-face` metric overrides (`size-adjust`,
  `ascent-override`).
