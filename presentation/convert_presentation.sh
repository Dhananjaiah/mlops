#!/bin/bash

# MLOps Course Presentation Converter
# This script helps convert the markdown presentation to various formats
# Usage: ./convert_presentation.sh [format]
# Formats: pptx, pdf, html, all

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INPUT_FILE="COURSE_PRESENTATION.md"
OUTPUT_BASE="MLOps_Course_Presentation"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command_exists marp; then
        missing_tools+=("marp")
    fi
    
    if ! command_exists pandoc; then
        missing_tools+=("pandoc")
    fi
    
    if ! command_exists reveal-md; then
        missing_tools+=("reveal-md")
    fi
    
    if [ ${#missing_tools[@]} -eq 3 ]; then
        print_error "No conversion tools found!"
        print_info "Please install at least one of the following:"
        print_info "  - Marp CLI: npm install -g @marp-team/marp-cli"
        print_info "  - Pandoc: https://pandoc.org/installing.html"
        print_info "  - reveal-md: npm install -g reveal-md"
        exit 1
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_warning "Some tools are not installed: ${missing_tools[*]}"
        print_info "Install them for more conversion options"
    fi
    
    print_success "Prerequisites check complete"
}

# Function to convert to PowerPoint using Marp
convert_to_pptx_marp() {
    if command_exists marp; then
        print_info "Converting to PowerPoint using Marp..."
        marp "$INPUT_FILE" --pptx --allow-local-files -o "${OUTPUT_BASE}.pptx"
        print_success "Created: ${OUTPUT_BASE}.pptx"
        return 0
    fi
    return 1
}

# Function to convert to PowerPoint using Pandoc
convert_to_pptx_pandoc() {
    if command_exists pandoc; then
        print_info "Converting to PowerPoint using Pandoc..."
        pandoc "$INPUT_FILE" -o "${OUTPUT_BASE}_pandoc.pptx"
        print_success "Created: ${OUTPUT_BASE}_pandoc.pptx"
        return 0
    fi
    return 1
}

# Function to convert to PDF
convert_to_pdf() {
    if command_exists marp; then
        print_info "Converting to PDF using Marp..."
        marp "$INPUT_FILE" --pdf --allow-local-files -o "${OUTPUT_BASE}.pdf"
        print_success "Created: ${OUTPUT_BASE}.pdf"
        return 0
    elif command_exists pandoc; then
        print_info "Converting to PDF using Pandoc..."
        pandoc "$INPUT_FILE" -o "${OUTPUT_BASE}.pdf"
        print_success "Created: ${OUTPUT_BASE}.pdf"
        return 0
    fi
    print_warning "No tool available for PDF conversion"
    return 1
}

# Function to convert to HTML
convert_to_html() {
    if command_exists marp; then
        print_info "Converting to HTML using Marp..."
        marp "$INPUT_FILE" --html --allow-local-files -o "${OUTPUT_BASE}.html"
        print_success "Created: ${OUTPUT_BASE}.html"
        return 0
    elif command_exists reveal-md; then
        print_info "Converting to HTML using reveal-md..."
        reveal-md "$INPUT_FILE" --static "${OUTPUT_BASE}_html"
        print_success "Created: ${OUTPUT_BASE}_html/"
        return 0
    elif command_exists pandoc; then
        print_info "Converting to HTML using Pandoc..."
        pandoc "$INPUT_FILE" -o "${OUTPUT_BASE}.html"
        print_success "Created: ${OUTPUT_BASE}.html"
        return 0
    fi
    print_warning "No tool available for HTML conversion"
    return 1
}

# Function to start reveal.js presentation
start_reveal() {
    if command_exists reveal-md; then
        print_info "Starting reveal.js presentation..."
        print_info "Press Ctrl+C to stop the server"
        reveal-md "$INPUT_FILE"
    else
        print_error "reveal-md is not installed"
        print_info "Install with: npm install -g reveal-md"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    cat << EOF
MLOps Course Presentation Converter

Usage: $0 [format]

Formats:
  pptx      Convert to PowerPoint (.pptx)
  pdf       Convert to PDF
  html      Convert to HTML
  reveal    Start reveal.js presentation server
  all       Convert to all available formats
  help      Show this help message

Examples:
  $0 pptx      # Convert to PowerPoint
  $0 all       # Convert to all formats
  $0 reveal    # Start presentation server

Prerequisites:
  Install at least one of these tools:
  - Marp CLI: npm install -g @marp-team/marp-cli
  - Pandoc: https://pandoc.org/installing.html
  - reveal-md: npm install -g reveal-md

For more information, see HOW_TO_CONVERT.md

EOF
}

# Main script logic
main() {
    # Change to presentation directory if not already there
    if [ ! -f "$INPUT_FILE" ]; then
        if [ -f "presentation/$INPUT_FILE" ]; then
            cd presentation
        else
            print_error "Cannot find $INPUT_FILE"
            print_info "Please run this script from the repository root or presentation directory"
            exit 1
        fi
    fi
    
    # Parse arguments
    FORMAT="${1:-help}"
    
    case "$FORMAT" in
        pptx)
            check_prerequisites
            convert_to_pptx_marp || convert_to_pptx_pandoc
            ;;
        pdf)
            check_prerequisites
            convert_to_pdf
            ;;
        html)
            check_prerequisites
            convert_to_html
            ;;
        reveal)
            start_reveal
            ;;
        all)
            check_prerequisites
            print_info "Converting to all available formats..."
            convert_to_pptx_marp || convert_to_pptx_pandoc
            convert_to_pdf
            convert_to_html
            print_success "All conversions complete!"
            ;;
        help|--help|-h|"")
            show_usage
            ;;
        *)
            print_error "Unknown format: $FORMAT"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
