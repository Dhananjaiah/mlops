# MLOps Course Presentation Materials

This directory contains presentation materials to help explain the MLOps course to students in an easy-to-understand format.

## 📁 Contents

- **COURSE_PRESENTATION.md** - 50+ slide markdown presentation covering the entire course
- **HOW_TO_CONVERT.md** - Step-by-step guide to convert markdown to PowerPoint
- **README.md** - This file

## 🎯 What's Included

The presentation covers:
- Course overview and structure (15 modules)
- Detailed breakdown of each module
- System architecture diagrams
- Technology stack
- Hands-on examples and code snippets
- Career paths and learning outcomes
- Assessment strategy
- Quick start guides
- Troubleshooting tips
- Community and support information

## 📊 Presentation Structure

The presentation is organized into 50+ slides:

1. **Slides 1-3**: Course Overview & Architecture
2. **Slides 4-17**: Detailed Module Breakdown (Modules 00-14)
3. **Slides 18-22**: Capstone Project & Career Opportunities
4. **Slides 23-28**: Learning Paths & Getting Started
5. **Slides 29-35**: Repository Structure & Best Practices
6. **Slides 36-40**: Prerequisites & Teaching Guide
7. **Slides 41-50**: Success Stories, Resources & Getting Started

## 🔄 Converting to PowerPoint

There are multiple ways to convert the markdown presentation to PowerPoint format:

### Method 1: Using Marp (Recommended)

Marp is a markdown presentation ecosystem that creates beautiful slides.

**Installation:**
```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Or using Docker
docker pull marpteam/marp-cli
```

**Conversion:**
```bash
# Convert to PowerPoint
marp COURSE_PRESENTATION.md --pptx -o MLOps_Course_Presentation.pptx

# Convert to PDF (alternative)
marp COURSE_PRESENTATION.md --pdf -o MLOps_Course_Presentation.pdf

# Convert to HTML
marp COURSE_PRESENTATION.md --html -o MLOps_Course_Presentation.html
```

**With Docker:**
```bash
docker run --rm -v $(pwd):/home/marp/app/ marpteam/marp-cli \
  COURSE_PRESENTATION.md --pptx -o MLOps_Course_Presentation.pptx
```

### Method 2: Using Pandoc

Pandoc is a universal document converter.

**Installation:**
```bash
# On Ubuntu/Debian
sudo apt-get install pandoc

# On macOS
brew install pandoc

# On Windows
# Download from https://pandoc.org/installing.html
```

**Conversion:**
```bash
# Convert to PowerPoint
pandoc COURSE_PRESENTATION.md -o MLOps_Course_Presentation.pptx

# With custom reference template
pandoc COURSE_PRESENTATION.md --reference-doc=template.pptx -o MLOps_Course_Presentation.pptx
```

### Method 3: Using reveal.js (Web-Based Slides)

For interactive web-based presentations:

**Installation:**
```bash
npm install -g reveal-md
```

**Usage:**
```bash
# Present slides in browser
reveal-md COURSE_PRESENTATION.md

# Export to PDF
reveal-md COURSE_PRESENTATION.md --print MLOps_Course_Presentation.pdf

# Export static HTML
reveal-md COURSE_PRESENTATION.md --static MLOps_Course_Presentation_html
```

### Method 4: Using Google Slides Importer

1. Convert markdown to HTML first:
   ```bash
   pandoc COURSE_PRESENTATION.md -o presentation.html
   ```

2. Open Google Slides
3. Go to File → Import slides
4. Upload the HTML file
5. Adjust formatting as needed

### Method 5: Manual Copy-Paste

If you prefer full control over formatting:

1. Open PowerPoint or Google Slides
2. Create a new presentation
3. Copy each slide section from the markdown
4. Paste into individual slides
5. Format with your preferred theme
6. Add images, diagrams, and custom graphics

## 🎨 Customization Tips

### Adding Your Branding

1. **Logo**: Add your organization's logo to the master slide
2. **Colors**: Update the color scheme to match your branding
3. **Fonts**: Choose fonts that align with your style guide
4. **Footer**: Add page numbers, course name, date

### Enhancing Visual Appeal

1. **Images**: Add relevant images for each module
   - Architecture diagrams
   - Tool logos (MLflow, DVC, Kubernetes, etc.)
   - Screenshots of interfaces
   - Workflow visualizations

2. **Icons**: Use icons for:
   - ✅ Learning outcomes
   - 🎯 Key takeaways
   - ⚠️ Important notes
   - 💡 Tips and best practices

3. **Code Highlighting**: Use proper syntax highlighting for code blocks

4. **Animations**: Add subtle animations for:
   - Bullet point reveals
   - Architecture flow diagrams
   - Step-by-step processes

## 📝 Using the Presentation

### For Instructors

**Before Class:**
- Review all slides and update with current examples
- Test all code snippets in your environment
- Prepare live demos for key concepts
- Customize slides with your teaching style

**During Class:**
- Use slides as a guide, not a script
- Pause for live coding demonstrations
- Encourage questions after each major section
- Show real troubleshooting examples

**After Class:**
- Share slide deck with students
- Provide additional resources
- Collect feedback for improvements

### For Self-Study

**Study Approach:**
1. Review 2-3 slides per session
2. Follow the code examples
3. Complete the mini-labs
4. Take notes on key concepts
5. Review troubleshooting sections

**Active Learning:**
- Type out code examples (don't just read)
- Pause and predict what happens next
- Try variations of commands
- Break things and fix them

## 🎓 For Different Audiences

### Tailoring the Presentation

**For Beginners:**
- Spend more time on slides 4-6 (foundations)
- Include extra examples
- Add more visual aids
- Slow down the pace

**For Intermediate:**
- Skip basic setup slides
- Focus on slides 8-16 (pipelines & production)
- Deep dive into architecture
- Share advanced troubleshooting

**For Advanced:**
- Focus on slides 13-17 (production concerns)
- Discuss architecture trade-offs
- Share production war stories
- Cover edge cases and optimizations

**For Executives:**
- Focus on slides 1-2, 18, 22 (overview & outcomes)
- Emphasize business value
- Show ROI and efficiency gains
- Highlight career development

## 📋 Presentation Modes

### Lecture Mode (1-2 hours)
Use slides: 1-3, 4-17 (key highlights), 18-22, 45-50
- Overview of entire course
- Module highlights only
- Career opportunities
- Getting started

### Workshop Mode (Full day)
Use all slides with extended demos
- Deep dive into each module
- Live coding sessions
- Hands-on exercises
- Troubleshooting practice

### Quick Intro (15-30 minutes)
Use slides: 1-3, 18-19, 22-23, 28, 45-46, 50
- Quick overview
- Key technologies
- Time commitment
- Getting started

### Career Talk (45 minutes)
Use slides: 1-2, 17-23, 31, 41-42, 46
- Course outcomes
- Career paths and salaries
- Success stories
- Certifications
- Next steps

## 🔧 Technical Requirements

### For Presenting

**Hardware:**
- Computer with 8GB+ RAM
- Projector or large display
- Backup laptop (recommended)
- Internet connection (for demos)

**Software:**
- PowerPoint, Keynote, or Google Slides
- Docker Desktop (for live demos)
- Code editor (VS Code recommended)
- Terminal/Command prompt

**Preparation:**
- Test all demos before presenting
- Have docker-compose stack running
- Prepare backup slides in case of issues
- Download any required resources

## 📚 Additional Resources

### Presentation Tools

**Markdown Presentation Frameworks:**
- Marp: https://marp.app/
- reveal.js: https://revealjs.com/
- GitPitch: https://gitpitch.com/
- Slidev: https://sli.dev/

**Design Tools:**
- Canva (for custom graphics)
- Figma (for diagrams)
- draw.io (for architecture diagrams)
- Excalidraw (for sketches)

**Code Screenshot Tools:**
- Carbon (carbon.now.sh)
- CodeSnap (VS Code extension)
- Ray.so

### Architecture Diagram Tools

Create visual diagrams for slides:
- **Lucidchart**: Professional diagrams
- **draw.io**: Free, open-source
- **Mermaid**: Markdown-based diagrams
- **PlantUML**: Code-based diagrams
- **Excalidraw**: Hand-drawn style

## 🎬 Live Demo Preparation

### Essential Demos to Prepare

1. **Module 02**: Environment setup with uv/poetry
2. **Module 03**: DVC data versioning
3. **Module 04**: MLflow experiment tracking
4. **Module 05**: Airflow DAG execution
5. **Module 08**: FastAPI model serving
6. **Module 11**: Grafana dashboard
7. **Module 12**: Drift detection with Evidently

### Demo Setup Checklist

- [ ] Docker Compose stack running
- [ ] Sample data loaded
- [ ] MLflow UI accessible
- [ ] API endpoints tested
- [ ] Grafana dashboards created
- [ ] Backup terminal logs ready
- [ ] Error scenarios prepared

## 💡 Pro Tips

### Presentation Tips

1. **Start Strong**: Begin with slide 3 (architecture) to show the big picture
2. **Live Demos**: Show actual tools, not just slides
3. **Tell Stories**: Share real production examples
4. **Encourage Questions**: Pause frequently
5. **Show Failures**: Demonstrate how to troubleshoot
6. **Provide Context**: Connect each module to real-world use cases

### Engagement Strategies

1. **Polls**: Ask "Who has used Docker/Kubernetes?"
2. **Quick Quiz**: Test understanding with module quizzes
3. **Pair Programming**: Have students work in pairs for labs
4. **Show & Tell**: Invite students to share their projects
5. **Office Hours**: Offer help sessions after class

### Common Questions to Prepare For

1. "How is this different from traditional software development?"
2. "Do I need to know machine learning?"
3. "Which cloud provider should I use?"
4. "How long will it take to complete the course?"
5. "What jobs can I get after this course?"
6. "Is the course material updated regularly?"

## 📞 Support

If you need help with the presentation materials:

- **Issues**: Open an issue on GitHub
- **Discussions**: Ask in GitHub Discussions
- **Pull Requests**: Suggest improvements
- **Email**: Contact course maintainer

## 📄 License

This presentation is part of the MLOps course and is licensed under the MIT License. Feel free to use, modify, and distribute with attribution.

## 🙏 Attribution

When using these materials, please include:

> **MLOps Course Presentation**
> From: https://github.com/Dhananjaiah/mlops
> License: MIT

---

**Happy Teaching! 🎓**

For the complete course content, see the main [README.md](../README.md) in the repository root.
