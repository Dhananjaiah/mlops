# How to Convert the Markdown Presentation to PowerPoint

This guide provides step-by-step instructions for converting the `COURSE_PRESENTATION.md` file into various presentation formats, with a focus on PowerPoint.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Method 1: Marp (Recommended)](#method-1-marp-recommended)
3. [Method 2: Pandoc](#method-2-pandoc)
4. [Method 3: reveal.js](#method-3-revealjs)
5. [Method 4: Google Slides](#method-4-google-slides)
6. [Customization Guide](#customization-guide)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

**Fastest way to get a PowerPoint file:**

```bash
# Install Marp CLI (one-time setup)
npm install -g @marp-team/marp-cli

# Convert to PowerPoint
cd presentation/
marp COURSE_PRESENTATION.md --pptx -o MLOps_Course_Presentation.pptx
```

Done! You now have a PowerPoint file ready to use and customize.

---

## Method 1: Marp (Recommended)

Marp creates beautiful, modern slides from markdown with excellent PowerPoint export.

### Step 1: Install Marp CLI

**Option A: Using npm (Node.js required)**
```bash
# Install Node.js first if you don't have it
# Download from: https://nodejs.org/

# Install Marp CLI globally
npm install -g @marp-team/marp-cli

# Verify installation
marp --version
```

**Option B: Using Docker (no Node.js needed)**
```bash
# Pull Marp Docker image
docker pull marpteam/marp-cli:latest

# Verify installation
docker run --rm marpteam/marp-cli --version
```

**Option C: Using Homebrew (macOS)**
```bash
brew install marp-cli
```

### Step 2: Basic Conversion

```bash
# Navigate to presentation directory
cd /path/to/mlops/presentation

# Convert to PowerPoint
marp COURSE_PRESENTATION.md --pptx -o MLOps_Course_Presentation.pptx
```

**With Docker:**
```bash
docker run --rm -v $(pwd):/home/marp/app/ marpteam/marp-cli \
  COURSE_PRESENTATION.md --pptx -o MLOps_Course_Presentation.pptx
```

### Step 3: Advanced Options

**Convert with custom theme:**
```bash
# Create a custom theme file (theme.css)
marp COURSE_PRESENTATION.md --theme theme.css --pptx -o output.pptx
```

**Convert with better quality:**
```bash
marp COURSE_PRESENTATION.md --pptx --allow-local-files -o output.pptx
```

**Convert to multiple formats:**
```bash
# PowerPoint
marp COURSE_PRESENTATION.md --pptx -o slides.pptx

# PDF
marp COURSE_PRESENTATION.md --pdf -o slides.pdf

# HTML
marp COURSE_PRESENTATION.md --html -o slides.html
```

### Step 4: Customize the Result

Open the generated PowerPoint file and:
1. Apply your organization's theme
2. Add your logo to the master slide
3. Adjust fonts and colors
4. Add images and diagrams
5. Fine-tune slide layouts

---

## Method 2: Pandoc

Pandoc is a universal document converter that supports many formats.

### Step 1: Install Pandoc

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install pandoc
```

**macOS:**
```bash
brew install pandoc
```

**Windows:**
Download installer from: https://pandoc.org/installing.html

**Verify installation:**
```bash
pandoc --version
```

### Step 2: Basic Conversion

```bash
# Navigate to presentation directory
cd /path/to/mlops/presentation

# Convert to PowerPoint
pandoc COURSE_PRESENTATION.md -o MLOps_Course_Presentation.pptx
```

### Step 3: Use a Custom Template

**Create a reference template:**
1. Create a PowerPoint file with your desired style
2. Save it as `template.pptx`
3. Use it as a reference:

```bash
pandoc COURSE_PRESENTATION.md \
  --reference-doc=template.pptx \
  -o MLOps_Course_Presentation.pptx
```

### Step 4: Advanced Options

**Control slide breaks:**
```bash
pandoc COURSE_PRESENTATION.md \
  --slide-level=2 \
  -o output.pptx
```

**Add metadata:**
```bash
pandoc COURSE_PRESENTATION.md \
  --metadata title="MLOps Course" \
  --metadata author="Your Name" \
  -o output.pptx
```

**Specify output format explicitly:**
```bash
pandoc COURSE_PRESENTATION.md \
  -t pptx \
  -o output.pptx
```

---

## Method 3: reveal.js

Create beautiful, interactive web-based slides.

### Step 1: Install reveal-md

```bash
# Install globally
npm install -g reveal-md

# Verify installation
reveal-md --version
```

### Step 2: Present Slides

**Start presentation server:**
```bash
# Navigate to presentation directory
cd /path/to/mlops/presentation

# Present slides in browser
reveal-md COURSE_PRESENTATION.md

# Custom port
reveal-md COURSE_PRESENTATION.md --port 3000
```

This opens the presentation in your browser at http://localhost:1948

### Step 3: Export to Static Files

**Export to PDF:**
```bash
reveal-md COURSE_PRESENTATION.md --print MLOps_Course_Presentation.pdf
```

**Export to static HTML:**
```bash
reveal-md COURSE_PRESENTATION.md --static _site
```

**Export as single HTML file:**
```bash
reveal-md COURSE_PRESENTATION.md --static _site --static-dirs=images
```

### Step 4: Customize Theme

**Use built-in themes:**
```bash
reveal-md COURSE_PRESENTATION.md --theme night
# Themes: black, white, league, beige, sky, night, serif, simple, solarized
```

**Use custom CSS:**
```bash
reveal-md COURSE_PRESENTATION.md --css custom.css
```

### Step 5: Advanced Features

**With speaker notes:**
```bash
reveal-md COURSE_PRESENTATION.md --separator "^---$" --vertical-separator "^--$"
```

**Watch mode (auto-reload):**
```bash
reveal-md COURSE_PRESENTATION.md --watch
```

**Full-screen mode:**
Press `F` during presentation

---

## Method 4: Google Slides

Import the presentation into Google Slides for cloud-based editing.

### Option A: Via HTML Import

**Step 1: Convert to HTML**
```bash
pandoc COURSE_PRESENTATION.md -o presentation.html
```

**Step 2: Import to Google Slides**
1. Go to https://slides.google.com
2. Click "Blank" to create a new presentation
3. Go to File → Import slides
4. Click "Upload" tab
5. Select `presentation.html`
6. Click "Import slides"

### Option B: Manual Copy-Paste

**Step 1: Prepare the Content**
1. Open `COURSE_PRESENTATION.md` in a text editor
2. Identify slide boundaries (marked by `---`)

**Step 2: Create Slides**
1. Go to https://slides.google.com
2. Create a new presentation
3. For each slide section:
   - Create a new slide
   - Copy the markdown content
   - Paste and format manually

**Step 3: Format**
1. Apply a theme (Slide → Change theme)
2. Format text (headings, bullets, code)
3. Add images and diagrams
4. Adjust layouts

### Option C: Use Google Docs as Intermediate

**Step 1: Convert to Google Docs**
```bash
pandoc COURSE_PRESENTATION.md -o presentation.docx
```

**Step 2: Import to Google Docs**
1. Go to https://docs.google.com
2. Click "Blank" to create a new document
3. Go to File → Open
4. Upload `presentation.docx`

**Step 3: Convert to Slides**
1. In Google Docs, select content for a slide
2. Copy
3. Switch to Google Slides
4. Paste
5. Repeat for each slide

---

## Customization Guide

### Adding Marp Directives

Add these at the top of `COURSE_PRESENTATION.md`:

```markdown
---
marp: true
theme: default
paginate: true
header: 'MLOps Course: 0→1→Production'
footer: 'Copyright © 2024 | github.com/Dhananjaiah/mlops'
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
---
```

### Custom Theme with Marp

**Create `theme.css`:**
```css
/* @theme mlops */

section {
  background-color: #f5f5f5;
  font-family: 'Arial', sans-serif;
}

h1 {
  color: #2563eb;
  border-bottom: 3px solid #2563eb;
}

h2 {
  color: #1e40af;
}

code {
  background-color: #e5e7eb;
  padding: 2px 6px;
  border-radius: 3px;
}

pre {
  background-color: #1f2937;
  color: #f3f4f6;
  padding: 1em;
  border-radius: 8px;
}

a {
  color: #2563eb;
  text-decoration: none;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  border: 1px solid #d1d5db;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #2563eb;
  color: white;
}
```

**Use the theme:**
```bash
marp COURSE_PRESENTATION.md --theme theme.css --pptx -o output.pptx
```

### Adding Images

**Method 1: Add to Markdown**
```markdown
## Slide Title

![Architecture Diagram](./images/architecture.png)

Content here...
```

**Method 2: Add After Conversion**
1. Convert to PowerPoint
2. Open the file
3. Insert → Picture
4. Add images to appropriate slides

### Custom PowerPoint Template

**Create template.pptx:**
1. Open PowerPoint
2. Go to View → Slide Master
3. Customize:
   - Fonts
   - Colors
   - Logo placement
   - Background
   - Layouts
4. Save as `template.pptx`

**Use template:**
```bash
pandoc COURSE_PRESENTATION.md \
  --reference-doc=template.pptx \
  -o MLOps_Course_Presentation.pptx
```

---

## Troubleshooting

### Issue: Marp CLI not found

**Solution:**
```bash
# Check if npm is installed
npm --version

# If not, install Node.js from https://nodejs.org/

# Install Marp CLI again
npm install -g @marp-team/marp-cli

# If permission error on Linux/Mac
sudo npm install -g @marp-team/marp-cli
```

### Issue: Pandoc not converting properly

**Solution:**
```bash
# Try explicit format specification
pandoc COURSE_PRESENTATION.md -f markdown -t pptx -o output.pptx

# Try with different slide level
pandoc COURSE_PRESENTATION.md --slide-level=2 -o output.pptx
```

### Issue: Code blocks not formatting correctly

**Solution for Marp:**
```bash
# Add syntax highlighting
marp COURSE_PRESENTATION.md --pptx --html -o output.pptx
```

**Solution for Pandoc:**
- Use a reference template with code style defined
- Or convert to HTML first, then import

### Issue: Tables not rendering

**Solution:**
- Ensure tables have proper markdown syntax
- Check for alignment issues
- Try converting to HTML first to verify

### Issue: Images not showing

**Solution:**
```bash
# For Marp, use --allow-local-files
marp COURSE_PRESENTATION.md --allow-local-files --pptx -o output.pptx

# For Pandoc, ensure image paths are correct
# Use absolute paths or relative paths from markdown location
```

### Issue: Slide breaks in wrong places

**Solution for Marp:**
- Use `---` for slide breaks
- Add `<!-- _class: lead -->` for special slides

**Solution for Pandoc:**
```bash
# Control slide breaks with --slide-level
pandoc COURSE_PRESENTATION.md --slide-level=2 -o output.pptx
```

### Issue: Docker permission denied

**Solution (Linux/Mac):**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker

# Try command again
docker run --rm -v $(pwd):/home/marp/app/ marpteam/marp-cli \
  COURSE_PRESENTATION.md --pptx -o output.pptx
```

---

## Best Practices

### Before Converting

1. **Review the markdown file**
   - Check for formatting issues
   - Ensure slide breaks are correct
   - Verify code blocks are properly formatted

2. **Prepare assets**
   - Collect images and diagrams
   - Create a theme/template if needed
   - Prepare logos and branding

3. **Test conversion**
   - Try converting 1-2 slides first
   - Check the output
   - Adjust before converting all slides

### After Converting

1. **Review all slides**
   - Check formatting
   - Ensure code is readable
   - Verify tables are correct

2. **Add visual elements**
   - Insert images
   - Add diagrams
   - Include charts

3. **Polish**
   - Apply consistent formatting
   - Add transitions (sparingly)
   - Test presentation flow

4. **Test**
   - Run through entire presentation
   - Check on actual presentation hardware
   - Ensure all features work

---

## Additional Tools

### Presentation Enhancers

**Diagrams:**
- draw.io: https://draw.io/
- Lucidchart: https://lucidchart.com/
- Mermaid: https://mermaid-js.github.io/

**Code Screenshots:**
- Carbon: https://carbon.now.sh/
- Ray.so: https://ray.so/

**Icons:**
- Font Awesome: https://fontawesome.com/
- Heroicons: https://heroicons.com/
- Lucide: https://lucide.dev/

**Stock Images:**
- Unsplash: https://unsplash.com/
- Pexels: https://pexels.com/

---

## Quick Reference

### Marp Commands
```bash
# PowerPoint
marp file.md --pptx -o output.pptx

# PDF
marp file.md --pdf -o output.pdf

# HTML
marp file.md --html -o output.html

# With theme
marp file.md --theme theme.css --pptx -o output.pptx

# Watch mode
marp file.md --watch
```

### Pandoc Commands
```bash
# PowerPoint
pandoc file.md -o output.pptx

# With template
pandoc file.md --reference-doc=template.pptx -o output.pptx

# Control slides
pandoc file.md --slide-level=2 -o output.pptx

# PDF via LaTeX
pandoc file.md -o output.pdf
```

### reveal-md Commands
```bash
# Present
reveal-md file.md

# Export PDF
reveal-md file.md --print output.pdf

# Static site
reveal-md file.md --static _site

# With theme
reveal-md file.md --theme night
```

---

## Getting Help

If you encounter issues:

1. **Check documentation:**
   - Marp: https://marp.app/
   - Pandoc: https://pandoc.org/
   - reveal-md: https://github.com/webpro/reveal-md

2. **Search for solutions:**
   - GitHub Issues for the respective tools
   - Stack Overflow
   - Tool-specific forums

3. **Ask for help:**
   - Open an issue in the MLOps course repo
   - Ask in GitHub Discussions
   - Contact course maintainers

---

**Happy Converting! 🎨**

Remember: The markdown file is the source of truth. Keep it updated, and you can always regenerate the PowerPoint file.
