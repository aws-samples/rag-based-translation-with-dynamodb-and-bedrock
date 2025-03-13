#!/bin/bash

# Start backend server
echo "Starting backend server..."
cd backend
python -m uvicorn main:app --reload &
BACKEND_PID=$!

# Wait a bit for backend to initialize
sleep 2

# Start frontend server
echo "Starting frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register the cleanup function for when script is terminated
trap cleanup SIGINT SIGTERM

# Keep script running
echo "Servers are running. Press Ctrl+C to stop."
wait
