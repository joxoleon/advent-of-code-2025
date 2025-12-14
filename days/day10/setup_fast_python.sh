#!/bin/bash

echo "Setting up fast Python compilation options..."

# Option 1: Install PyPy (JIT-compiled Python - often 5-10x faster)
echo "Installing PyPy3..."
brew install pypy3

# Option 2: Install Nuitka (Python to C++ compiler)
echo "Installing Nuitka..."
python3 -m pip install --user nuitka

echo ""
echo "Usage options:"
echo ""
echo "1. Run with PyPy (JIT compilation):"
echo "   pypy3 pt2_optimized.py"
echo ""
echo "2. Compile with Nuitka (Python to C++):"
echo "   python3 -m nuitka --standalone --onefile pt2_optimized.py"
echo "   ./pt2_optimized.bin"
echo ""
echo "3. Use the memoized version:"
echo "   python3 pt2_optimized.py"