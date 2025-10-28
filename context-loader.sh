#!/bin/bash
# context-loader.sh - Load InquiryCircle project context for AI sessions
# Usage: ./context-loader.sh

set -e  # Exit on any error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Documentation path
DOCS_PATH="/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/Documentation"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

echo
print_info "Loading InquiryCircle project context from DOCS-ENV..."
echo

# Check if documentation directory exists
if [ ! -d "$DOCS_PATH" ]; then
    print_warning "Documentation directory not found at: $DOCS_PATH"
    exit 1
fi

print_info "Documentation source: $DOCS_PATH"
echo

# Load core project files in order
print_status "Loading project specification..."
cat "$DOCS_PATH/project-spec.md"
echo -e "\n---\n"

print_status "Loading current status..."
cat "$DOCS_PATH/STATUS.md"
echo -e "\n---\n"

print_status "Loading operations guide..."
cat "$DOCS_PATH/operations-guide.md"
echo -e "\n---\n"

print_status "Loading operations guide 2 (operation directives)..."
cat "$DOCS_PATH/operations-guide2.md"
echo -e "\n---\n"

print_status "Loading infrastructure documentation..."
cat "$DOCS_PATH/infrastructure.md"
echo -e "\n---\n"

print_status "Loading changelog..."
cat "$DOCS_PATH/CHANGELOG.md"
echo

print_info "📋 Context loading complete!"
print_info "🤖 AI Session Ready - InquiryCircle project context loaded"
echo
print_info "💡 Key Information Loaded:"
echo "   • Project architecture and constraints"
echo "   • Current development status and priorities"
echo "   • Complete operations procedures and commands"
echo "   • Operation directives (streamlined commands)"
echo "   • Infrastructure setup and environments"
echo "   • Documentation change history"
echo
print_info "🚀 Ready to work on InquiryCircle!"