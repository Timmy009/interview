#!/usr/bin/env python3
"""
Script to create and apply migration for the due_date field in Loan model.
Run this script to update the database schema.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

def create_and_apply_migration():
    """Create and apply migration for the Loan model due_date field."""
    print("Creating migration for Loan model...")
    execute_from_command_line(['manage.py', 'makemigrations', 'library'])
    
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Migration completed successfully!")

if __name__ == '__main__':
    create_and_apply_migration()
