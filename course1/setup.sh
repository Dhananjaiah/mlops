#!/bin/bash

# MLOps Course Setup Script
# This script sets up your environment for the course

set -e  # Exit on error

echo "======================================================================"
echo "🚀 MLOps Course - Automated Setup"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the course1 directory"
    exit 1
fi

echo "📋 Step 1: Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3.11+ required, found $PYTHON_VERSION"
    exit 1
fi

echo ""
echo "📦 Step 2: Creating virtual environment..."
if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists, skipping creation"
else
    python -m venv .venv
    print_success "Virtual environment created"
fi

echo ""
echo "🔄 Step 3: Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

echo ""
echo "⬆️  Step 4: Upgrading pip..."
pip install --upgrade pip -q
print_success "pip upgraded"

echo ""
echo "📥 Step 5: Installing course dependencies..."
echo "   This may take 3-5 minutes..."
pip install -r requirements.txt -q
print_success "Dependencies installed"

echo ""
echo "🔍 Step 6: Verifying installation..."
cd module00-setup/code
python verify_setup.py

echo ""
echo "======================================================================"
echo "🎉 Setup Complete!"
echo "======================================================================"
echo ""
echo "📚 Next steps:"
echo "   1. Activate virtual environment:"
echo "      source .venv/bin/activate"
echo ""
echo "   2. Start with Module 00:"
echo "      cd module00-setup"
echo "      cat README.md"
echo ""
echo "   3. Run hello script:"
echo "      cd code"
echo "      python 01_hello_mlops.py"
echo ""
echo "======================================================================"
