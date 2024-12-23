#!/bin/bash

echo "Building and starting Docker containers..."
docker-compose up --build -d

echo "Application is running at http://localhost:5000"
