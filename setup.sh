#!/bin/bash

# ADK Sales Agent - Automated Setup Script
# This script sets up the development environment for the ADK Sales Agent API

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
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

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        return 1
    fi
}

# Create virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    source venv/bin/activate
    print_success "Virtual environment created and activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        return 1
    fi
    
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed successfully"
}

# Setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_warning "Created .env from .env.example template"
            print_warning "Please edit .env file with your actual Airtable API credentials"
        else
            print_status "Creating basic .env file..."
            cat > .env << EOF
# ADK Sales Agent API - Environment Variables
# Copy this file to .env and fill in your actual values

# AIRTABLE_API_KEY=your_airtable_api_key_here
AIRTABLE_BASE_ID=appYKRoIWJLctlUdw
AIRTABLE_LEADS_TABLE_ID=tblUZkxzC0MbJ12HG
AIRTABLE_CALLS_TABLE_ID=tblyyuYfdzGc0CAkO

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
EOF
            print_warning "Created basic .env file - please add your AIRTABLE_API_KEY"
        fi
    else
        print_success "Environment file (.env) already exists"
    fi
}

# Test API connectivity
test_api() {
    print_status "Testing API connectivity..."
    
    # Check if .env has API key
    if ! grep -q "^AIRTABLE_API_KEY=" .env || grep -q "^AIRTABLE_API_KEY=$" .env || grep -q "your_airtable_api_key_here" .env; then
        print_warning "AIRTABLE_API_KEY not configured. Skipping API connectivity test."
        print_warning "Please add your Airtable API key to .env file"
        return 0
    fi
    
    print_status "Starting API server for testing..."
    
    # Start the server in background
    python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 5
    
    # Test health endpoint
    if curl -s http://localhost:8000/ > /dev/null; then
        print_success "API server is responding"
        
        # Test Airtable connection
        if curl -s http://localhost:8000/config | grep -q "airtable"; then
            print_success "Airtable configuration loaded"
        else
            print_warning "Airtable configuration may have issues"
        fi
    else
        print_error "API server is not responding"
    fi
    
    # Stop the test server
    kill $SERVER_PID 2>/dev/null || true
    sleep 2
}

# Run tests
run_tests() {
    print_status "Running test suite..."
    
    if [ -f "test_api.py" ]; then
        python -m pytest test_api.py -v
        if [ $? -eq 0 ]; then
            print_success "All tests passed"
        else
            print_warning "Some tests failed - check configuration"
        fi
    else
        print_warning "No test file found (test_api.py)"
    fi
}

# Display final instructions
show_final_instructions() {
    print_header "Setup Complete!"
    
    echo -e "${GREEN}✅ Virtual environment created${NC}"
    echo -e "${GREEN}✅ Dependencies installed${NC}"
    echo -e "${GREEN}✅ Environment configuration ready${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Activate the virtual environment:"
    echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    echo ""
    echo "2. Edit .env file with your Airtable API key:"
    echo -e "   ${YELLOW}nano .env${NC}"
    echo ""
    echo "3. Start the development server:"
    echo -e "   ${YELLOW}uvicorn api.main:app --reload --host 0.0.0.0 --port 8000${NC}"
    echo ""
    echo "4. Access the API documentation:"
    echo -e "   ${YELLOW}http://localhost:8000/docs${NC}"
    echo ""
    echo "5. Run tests:"
    echo -e "   ${YELLOW}python -m pytest test_api.py -v${NC}"
    echo ""
    print_success "Happy coding! 🚀"
}

# Main setup function
main() {
    print_header "ADK Sales Agent - Setup Script"
    
    # Check if we're in the right directory
    if [ ! -f "api/main.py" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
    
    # Run setup steps
    check_python || exit 1
    setup_venv || exit 1
    install_dependencies || exit 1
    setup_environment || exit 1
    
    # Optional tests (don't fail setup if they fail)
    print_header "Running Optional Tests"
    test_api || true
    run_tests || true
    
    show_final_instructions
}

# Run main function
main "$@" 