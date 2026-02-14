#!/bin/bash

# CareOps Development Setup Script

echo "🚀 Starting CareOps Development Environment..."
echo ""

# Create backend .env if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env..."
    cp backend/.env.example backend/.env
fi

# Create frontend .env.local if it doesn't exist
if [ ! -f frontend/.env.local ]; then
    echo "Creating frontend/.env.local..."
    cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF
fi

# Install backend dependencies
echo ""
echo "📦 Installing backend dependencies..."
cd backend
pip install -q -r requirements.txt
cd ..

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install -q
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  Terminal 1: cd backend && python main.py"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
