#!/bin/bash

# English to Kannada Translator - Quick Start Script for macOS/Linux

clear

echo "======================================================"
echo "  English to Kannada Translator - Setup"
echo "======================================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python $(python3 --version | cut -d' ' -f2) detected"
echo ""

echo "Choose your setup option:"
echo ""
echo "1. Quick Start (Local Version - Recommended)"
echo "2. Google Cloud Setup"
echo "3. Install Dependencies Only"
echo "4. Run Application"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Installing local dependencies..."
        pip3 install -r requirements_local.txt
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Setup complete! Starting application..."
            python3 app_local.py
        else
            echo "❌ Error installing dependencies"
            exit 1
        fi
        ;;
    
    2)
        echo ""
        echo "Google Cloud Setup"
        echo ""
        read -p "Enter path to Google Cloud credentials JSON file: " cred_path
        
        if [ -f "$cred_path" ]; then
            export GOOGLE_APPLICATION_CREDENTIALS="$cred_path"
            echo ""
            echo "Installing Google Cloud dependencies..."
            pip3 install -r requirements.txt
            
            if [ $? -eq 0 ]; then
                echo ""
                echo "✅ Setup complete! Starting application..."
                python3 app.py
            else
                echo "❌ Error installing dependencies"
                exit 1
            fi
        else
            echo "❌ Error: Credentials file not found at $cred_path"
            exit 1
        fi
        ;;
    
    3)
        echo ""
        echo "1. Install Local Dependencies"
        echo "2. Install Google Cloud Dependencies"
        echo "3. Install Both"
        echo ""
        read -p "Enter your choice (1-3): " dep_choice
        
        case $dep_choice in
            1) pip3 install -r requirements_local.txt ;;
            2) pip3 install -r requirements.txt ;;
            3)
                pip3 install -r requirements_local.txt
                pip3 install -r requirements.txt
                ;;
        esac
        ;;
    
    4)
        echo ""
        echo "1. Run Local Version"
        echo "2. Run Google Cloud Version"
        echo ""
        read -p "Enter your choice (1-2): " app_choice
        
        case $app_choice in
            1) python3 app_local.py ;;
            2) python3 app.py ;;
        esac
        ;;
    
    5)
        echo "Exiting setup..."
        exit 0
        ;;
    
    *)
        echo "❌ Invalid choice. Please try again."
        exit 1
        ;;
esac
