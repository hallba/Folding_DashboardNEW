"""
Startup script for the Dash dashboard that fixes Jupyter integration issues
"""
import os

# Disable Jupyter mode for Dash (fixes NotImplementedError in non-Jupyter environments)
os.environ['JUPYTER_PLATFORM_DIRS'] = '0'

# Import and run the main application
import main
