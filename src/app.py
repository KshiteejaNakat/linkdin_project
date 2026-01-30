"""
Adaptive AI Career Architect
Main Application Entry Point
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_app import run_app

if __name__ == "__main__":
    run_app()
