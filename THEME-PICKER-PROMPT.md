# Prompt for Hercules — theme picker in the top bar

Add a theme control to the top bar so each person can choose how the platform
looks. Three themes, no more. This is frontend only — no schema change, no new
table, no backend work.

---

## 1. Where it goes

`src/components/layout/AppLayout.tsx`, around line 276, renders
`<NotificationPanel />` in the top bar. Put the theme control **immediately to
the left of the notification bell**, in the same row, same vertical alignment,
same icon-button size.

A single icon button that opens a small menu of the three themes, with the
current one marked. Not three separate buttons, and not a cycling toggle — a
person should be able to see which theme is active and pick another directly.

## 2. The three themes

Named in full in the interface. Section 4 of the master prompt forbids
abbreviations anywhere in the interface, so no "Lt", no "Dk", no ampersands.

| Value | Label shown to the person |
|---|---|
| `light` | Bright |
| `dark` | Dark |
| `magnus` | Magnus Green and Orange |

## 3. How to wire it

`next-themes` is already installed and configured in
`src/components/providers/theme.tsx` with `attribute="class"`. Extend it rather
than replacing it:

```tsx
<NextThemeProvider
  attribute="class"
  themes={["light", "dark", "magnus"]}
  defaultTheme="light"
  enableSystem={false}
  {...props}
>
```

Two deliberate changes from what is there now. `themes` must be declared or
`next-themes` will not apply a class other than `light` or `dark`. And
`enableSystem` goes to `false` with `defaultTheme="light"` — with three explicit
themes, following the operating system adds a hidden fourth state that the picker
cannot show, which makes the control confusing.

The choice is stored per browser in `localStorage`, which `next-themes` does
already. **Do not add a database field or a table for it.** If we later want the
choice to follow a person across devices, that is a separate decision.

Wrap the control in `next-themes`' mounted check so the first paint does not
flash the wrong theme.

## 4. The Magnus Green and Orange theme

`src/index.css` defines the palette as CSS custom properties: a `:root` block for
Bright and a `.dark` block at line 91 for Dark. Add a third block, `.magnus`,
defining **the same 32 variables**. Every variable present in `:root` must be
present in `.magnus` — a missing one falls through to the Bright value and the
theme breaks in one corner of one screen, which is the hardest kind of bug to
find later.

Cool green surfaces, Magnus orange for accent and focus. Starting values:

```css
.magnus {
  --radius: 0.5rem;
  --background: oklch(0.98 0.012 170);
  --foreground: oklch(0.20 0.030 175);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.20 0.030 175);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.20 0.030 175);
  --primary: oklch(0.42 0.090 170);
  --primary-foreground: oklch(0.98 0.010 170);
  --secondary: oklch(0.93 0.025 170);
  --secondary-foreground: oklch(0.30 0.060 172);
  --muted: oklch(0.94 0.018 170);
  --muted-foreground: oklch(0.50 0.030 172);
  --accent: oklch(0.70 0.170 52);
  --accent-foreground: oklch(0.20 0.045 45);
  --destructive: oklch(0.58 0.220 27);
  --border: oklch(0.87 0.022 170);
  --input: oklch(0.87 0.022 170);
  --ring: oklch(0.70 0.170 52);
  --chart-1: oklch(0.48 0.110 170);
  --chart-2: oklch(0.70 0.170 52);
  --chart-3: oklch(0.60 0.120 195);
  --chart-4: oklch(0.78 0.140 75);
  --chart-5: oklch(0.40 0.080 165);
  --sidebar: oklch(0.26 0.050 172);
  --sidebar-foreground: oklch(0.92 0.012 170);
  --sidebar-primary: oklch(0.72 0.170 52);
  --sidebar-primary-foreground: oklch(0.16 0.030 45);
  --sidebar-accent: oklch(0.34 0.060 172);
  --sidebar-accent-foreground: oklch(0.94 0.010 170);
  --sidebar-border: oklch(0.32 0.050 172);
  --sidebar-ring: oklch(0.70 0.150 52);
}
```

I have computed the contrast for every one of these pairings. All pass at 4.5:1
or better: body text on background 17.03:1, body text on card 17.96:1, muted text
16.03:1 (5.60:1), text on primary 7.57:1, sidebar text on sidebar 12.09:1.

**One correction is already applied above and matters.** An earlier draft used a
near-white `--accent-foreground` on the orange, which measures **2.73:1 and
fails.** The value given, `oklch(0.20 0.045 45)`, measures **6.47:1** — dark text
on orange, which is what the Bright and Dark themes already do (9.11:1 and
7.60:1). Do not change it back to a light value.

If you adjust any colour, recompute the contrast for every pairing that touches
it and report the numbers. Body text must reach 4.5:1 on its own background and
on cards, and any text on the accent must reach 4.5:1.

## 5. What must not break

- The existing Bright and Dark themes are unchanged. Do not edit `:root` or
  `.dark`.
- `src/components/ui/sonner.tsx` reads `useTheme()` for toast styling. Confirm
  toasts render correctly under `magnus` — it will not match `"dark"`, so make
  sure it falls back to the light treatment rather than to nothing.
- Every screen must be checked under all three themes, not only the dashboard.
  The heavy ones are `src/pages/admin/page.tsx`, `safety`, `inventory`,
  `permits`, `construction` and `manpower` — they carry the most custom colour.
- The `@custom-variant dark (&:is(.dark *))` rule at the top of `index.css`
  targets `.dark` only. Any component using `dark:` Tailwind variants will keep
  its Bright appearance under `magnus`, which is correct — but check nothing
  looks half-styled as a result.

## 6. Report back with

1. The file and line where the control was added.
2. Any colour values you changed from the starting set, and the contrast ratio
   you measured for each.
3. Confirmation that you opened all three themes on at least the six heavy pages
   named above, and what you found.

Screenshots if you can produce them.
