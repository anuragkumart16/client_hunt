#!/bin/bash

echo "Installing root dependencies..."
npm install

echo "Installing Backend dependencies..."
cd Backend
npm install
cd ..

echo "Installing Frontend dependencies..."
cd Frontend
npm install
cd ..

echo "Installing App dependencies..."
cd App
npm install
cd ..

echo "All dependencies installed successfully!" 