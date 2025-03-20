#! /bin/bash

function exit_on_error {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

function setup {
    echo "Setting up development environment..."
    echo "Creating python virtual environment..."
    python3 -m venv .venv
    exit_on_error "Failed to create python virtual environment"

    echo "Activating python virtual environment..."
    source .venv/bin/activate
    exit_on_error "Failed to activate python virtual environment"

    echo "Installing python dependencies..."
    pip install -r requirements.txt
    exit_on_error "Failed to install python dependencies"

    echo "Environment setup complete!"
}

function activate_env {
    if [ ! -d .venv ]; then
        echo "Error: Python virtual environment not found. Run 'bash main.sh setup' to create it."
        exit 1
    fi

    source .venv/bin/activate
    exit_on_error "Failed to activate python virtual environment"
}

function test {
    echo "Running tests..."
    pytest --cov=./src ./tests
    exit_on_error "Tests failed"
    echo "Tests passed!"
}

function build {
    echo "Building project..."
    
    echo "Building sdist..."
    python3 -m build --sdist
    exit_on_error "Failed to build sdist"
    
    echo "Building wheel..."
    python3 -m build --wheel
    exit_on_error "Failed to build wheel"

    echo "Build complete!"
}

function upload {
    echo "Checking validation..."
    twine check dist/*
    exit_on_error "Failed to validate project"

    echo "Uploading project..."
    twine upload dist/*
    exit_on_error "Failed to upload project to PyPI"
    echo "Upload complete!"
}

function clean {
    echo "Cleaning up..."
    rm -rf .venv
    rm -rf dist
    rm -rf build
    rm -rf *.egg-info
    echo "Cleanup complete!"
}

function main {
    if [ $1 == "setup" ]; then
        setup
        return
    fi

    activate_env

    case $1 in
        test)
            test
            ;;
        build)
            build
            ;;
        upload)
            upload
            ;;
        clean)
            clean
            ;;
        *)
            echo "Usage: $0 {setup|test|build|upload|clean}"
            exit 1
            ;;
    esac
}

main $@