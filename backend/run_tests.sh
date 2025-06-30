#!/bin/bash

# Test runner script for the AI Chat backend

echo "🧪 Running AI Chat Backend Tests"
echo "=================================="

# Function to run tests with coverage
run_tests_with_coverage() {
    echo "📊 Running tests with coverage..."
    pytest --cov=app --cov-report=term-missing --cov-report=html tests/
}

# Function to run tests without coverage
run_tests() {
    echo "⚡ Running tests..."
    pytest tests/
}

# Function to run specific test file
run_specific_test() {
    echo "🎯 Running specific test: $1"
    pytest tests/$1 -v
}

# Function to run tests with verbose output
run_tests_verbose() {
    echo "🔍 Running tests with verbose output..."
    pytest tests/ -v -s
}

# Check command line arguments
case "$1" in
    "coverage")
        run_tests_with_coverage
        ;;
    "verbose")
        run_tests_verbose
        ;;
    "file")
        if [ -z "$2" ]; then
            echo "❌ Please specify a test file: ./run_tests.sh file test_api.py"
            exit 1
        fi
        run_specific_test $2
        ;;
    "help"|"-h"|"--help")
        echo "Usage: ./run_tests.sh [option]"
        echo ""
        echo "Options:"
        echo "  (no args)  - Run tests normally"
        echo "  coverage   - Run tests with coverage report"
        echo "  verbose    - Run tests with verbose output"
        echo "  file <file> - Run specific test file"
        echo "  help       - Show this help message"
        ;;
    *)
        run_tests
        ;;
esac

echo ""
echo "✅ Tests completed!" 