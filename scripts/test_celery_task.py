#!/usr/bin/env python3
"""
Script to test the check_overdue_loans Celery task.
This creates test data and verifies the task execution.
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.contrib.auth.models import User
from library.models import Author, Book, Member, Loan
from library.tasks import check_overdue_loans

def create_test_data():
    """Create test data for overdue loan testing."""
    print("Creating test data...")
    
    # Create test user and member
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    member, created = Member.objects.get_or_create(user=user)
    
    # Create test author and book
    author, created = Author.objects.get_or_create(
        first_name='Test',
        last_name='Author',
        defaults={'biography': 'Test biography'}
    )
    book, created = Book.objects.get_or_create(
        title='Test Book',
        defaults={
            'author': author,
            'isbn': '1234567890123',
            'genre': 'fiction',
            'available_copies': 1
        }
    )
    
    # Create overdue loan (due date in the past)
    overdue_date = date.today() - timedelta(days=5)
    loan, created = Loan.objects.get_or_create(
        book=book,
        member=member,
        defaults={
            'due_date': overdue_date,
            'is_returned': False
        }
    )
    
    print(f"Created test loan with due date: {loan.due_date}")
    return loan

def test_overdue_task():
    """Test the check_overdue_loans task."""
    print("Testing check_overdue_loans task...")
    
    # Create test data
    loan = create_test_data()
    
    # Run the task
    result = check_overdue_loans.delay()
    print(f"Task result: {result.get()}")
    
    print("Test completed successfully!")

if __name__ == '__main__':
    test_overdue_task()
