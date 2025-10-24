#!/bin/bash
echo "🚀 Starting Daily Work Logger..."
echo

# Navigate to your app directory
cd "/mnt/c/Users/Admin/Desktop/DailyUpdates/DailyWorks" || {
  echo "❌ Directory not found!"
  exit 1
}

echo "📂 Current directory: $(pwd)"
echo
echo "▶️ Starting Streamlit app..."
streamlit run main.py

echo
read -p "Press Enter to exit..."
