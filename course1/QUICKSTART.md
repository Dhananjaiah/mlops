# Course 1 - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Quick Setup

```bash
# Clone the repository
git clone https://github.com/Dhananjaiah/mlops.git
cd mlops/course1

# Run automated setup
chmod +x setup.sh
./setup.sh

# Or manual setup:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Verify Your Setup

```bash
cd module00-setup/code
python verify_setup.py
```

Expected output:
```
✅ Python 3.11+ - OK
✅ Docker is running
✅ All dependencies installed
🎉 All checks passed! You're ready to start learning.
```

### 3. Start Learning

```bash
# Begin with Module 00
cd module00-setup
cat README.md

# Run the hello script
cd code
python 01_hello_mlops.py

# Move to Module 01
cd ../../module01-foundations
python code/01_ml_workflow.py
```

## 📚 Module Overview

### Module 00: Setup (30 min) ✅ COMPLETE
**What you get:**
- Verified development environment
- Understanding of course structure
- All tools installed and tested

**Files:**
- `README.md` - Module overview
- `transcript.md` - Complete lecture
- `code/verify_setup.py` - Environment verification
- `code/01_hello_mlops.py` - Course introduction
- `code/02_check_tools.py` - Tool checker

**What you'll learn:**
- What MLOps is and why it matters
- Course philosophy and structure
- Tools you'll master

### Module 01: MLOps Foundations (1 hour) ✅ COMPLETE
**What you get:**
- Complete ML workflow example
- Artifact tracking system
- Reproducibility demonstrations

**Files:**
- `README.md` - Learning objectives
- `code/01_ml_workflow.py` - End-to-end ML workflow
- `code/02_artifact_tracking.py` - Artifact tracking demo
- `code/03_reproducibility.py` - Reproducibility examples

**What you'll learn:**
- ML lifecycle stages
- Artifact tracking and lineage
- Why reproducibility matters
- Dev-prod parity concepts

### Module 02-08: Coming Soon 🚧
More modules are being developed with the same quality and integration!

## 🎯 What Makes This Course Special

### ✅ Single Source of Truth
- All code is tested and works together
- No broken dependencies or integration issues
- Everything properly "stitched together"

### ✅ Complete Transcripts
- Detailed explanations for every concept
- Real-world analogies
- Clear learning progression

### ✅ Working Code Examples
- Every script runs successfully
- Comprehensive documentation
- Follows best practices

### ✅ Hands-On Learning
- Practice exercises
- Solutions provided
- Build real skills

## 🔧 Testing Your Installation

### Quick Test
```bash
# From course1 directory
python module00-setup/code/01_hello_mlops.py
python module01-foundations/code/01_ml_workflow.py
```

### Expected Results
Both scripts should run without errors and produce:
- Welcome messages
- Educational content
- Generated artifacts (data, models, metrics)

### If You See Errors

**Missing module errors:**
```bash
pip install -r requirements.txt
```

**Permission errors:**
```bash
chmod +x setup.sh
```

**Python version errors:**
- Ensure Python 3.11+ is installed
- Check with: `python --version`

## 📖 How to Use This Course

### For Self-Learners

1. **Follow sequentially** - Each module builds on previous ones
2. **Read transcripts first** - Understand before coding
3. **Run all examples** - Hands-on practice is key
4. **Complete exercises** - Test your understanding
5. **Review solutions** - Learn different approaches

**Time commitment:**
- Module 00: 30 minutes
- Module 01: 1 hour
- Total so far: 1.5 hours
- Full course: ~25-30 hours

### For Instructors

Use this course to teach MLOps:
1. **Lecture material** - Transcripts have talking points
2. **Live demos** - Run code examples in class
3. **Assignments** - Use exercises as homework
4. **Assessment** - Check understanding
5. **Customization** - Adapt to your needs

### For Teams

Adopt MLOps practices:
1. **Pair programming** - Work through together
2. **Code reviews** - Review solutions
3. **Implementation** - Apply to real projects
4. **Knowledge sharing** - Teach each other
5. **Continuous learning** - Regular practice

## 🎓 Learning Tips

### Success Strategies

✅ **Set aside dedicated time** - 2-3 hours per module  
✅ **Practice daily** - Consistency beats intensity  
✅ **Ask questions** - No question is too basic  
✅ **Build projects** - Apply learnings immediately  
✅ **Join community** - Learn with others  

### Common Mistakes to Avoid

❌ **Skipping modules** - Don't skip ahead  
❌ **Just reading** - You must code to learn  
❌ **Giving up on errors** - Errors are learning  
❌ **Rushing** - Take your time  
❌ **Not taking breaks** - Rest helps retention  

## 🆘 Getting Help

### If You're Stuck

1. **Check the transcript** - Detailed explanations
2. **Read error messages** - They tell you what's wrong
3. **Review the code** - Compare with examples
4. **Search online** - Google the error
5. **Ask for help** - GitHub discussions/issues

### Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Permission denied"**
```bash
chmod +x setup.sh
```

**"Docker not found"**
- Install Docker Desktop from docker.com

**Code doesn't match output**
- Check you're in the right directory
- Verify Python version (3.11+)
- Reinstall requirements

## 📊 Progress Tracking

Track your completion:

- [ ] Module 00: Setup ✓
- [ ] Module 01: Foundations
  - [ ] Read README
  - [ ] Read transcript  
  - [ ] Run 01_ml_workflow.py
  - [ ] Run 02_artifact_tracking.py
  - [ ] Run 03_reproducibility.py
  - [ ] Complete exercises
- [ ] Module 02: Environment & Packaging (Coming Soon)
- [ ] Module 03: Data Versioning (Coming Soon)
- [ ] Module 04: Experiment Tracking (Coming Soon)
- [ ] Module 05: Pipelines (Coming Soon)
- [ ] Module 06: Training (Coming Soon)
- [ ] Module 07: Registry (Coming Soon)
- [ ] Module 08: Serving (Coming Soon)

## 🎯 What You'll Build

By the end of this course, you'll have:
- ✅ Working MLOps development environment
- ✅ Understanding of ML lifecycle
- ✅ Skills in versioning data and code
- ✅ Experience with experiment tracking
- ✅ Knowledge of pipeline automation
- ✅ Ability to deploy ML models
- ✅ Portfolio of MLOps projects

## 🚀 After Completion

### Next Steps
1. **Build portfolio projects** - Apply all concepts
2. **Contribute to open source** - MLflow, DVC, Airflow
3. **Get certified** - AWS ML, GCP ML Engineer
4. **Join MLOps community** - Attend meetups
5. **Share your journey** - Blog, talks, teaching

### Career Paths
- ML Engineer
- MLOps Engineer
- Platform Engineer
- Data Scientist (MLOps-savvy)
- ML Architect

## 📝 Feedback

We'd love your feedback!
- ⭐ Star the repository if helpful
- 🐛 Report issues or errors
- 💡 Suggest improvements
- 📝 Share success stories
- 🤝 Contribute via PR

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- MLOps community
- Open source maintainers
- Course contributors
- Student feedback

---

**Ready to start?**  
👉 [Begin with Module 00](module00-setup/README.md)

**Questions?**  
👉 Open an issue or discussion

**Let's build production ML systems together! 🚀**
