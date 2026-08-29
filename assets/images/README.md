# University Logo Setup

This directory contains the university logo for the website.

## Current Logo

The current logo (`unil-logo.svg`) is a placeholder SVG created for the University of Lausanne (UNIL).

## Replacing the Logo

To replace the logo with your university's actual logo:

1. **Prepare your logo file:**
   - Recommended formats: SVG (preferred), PNG, or JPG
   - Recommended dimensions: 200x60 pixels or similar aspect ratio
   - Name your file `unil-logo.svg` (or update the references in the code)

2. **Replace the file:**
   - Replace `/docs/assets/images/unil-logo.svg` with your logo file
   - If using a different format, update the file extension in:
     - `/docs/_includes/navigation.html` (line 3)
     - `/docs/index.html` (line 13)

3. **Adjust styling if needed:**
   - Logo sizing can be adjusted in `/docs/assets/css/style.scss`
   - Hero logo sizing can be adjusted in `/docs/index.html` (CSS section)

## Logo Placement

The logo appears in two places:
1. **Navigation header**: Next to the site title on every page
2. **Homepage hero section**: Large logo next to the main title

## Technical Details

- Logo height in navigation: 40px (desktop), 32px (mobile)
- Logo height in hero section: 80px (desktop), 60px (mobile)
- The logo is responsive and scales appropriately on different screen sizes
