#!/usr/bin/env python3
"""
Script to seed the database with sample data for testing.
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

def seed_database():
    """Seed the database with sample data."""
    print("Seeding database with sample data...")
    
    # Create sample authors
    authors_data = [
        {'first_name': 'Jane', 'last_name': 'Austen', 'biography': 'English novelist'},
        {'first_name': 'George', 'last_name': 'Orwell', 'biography': 'English author and journalist'},
        {'first_name': 'Agatha', 'last_name': 'Christie', 'biography': 'English writer of detective fiction'},
    ]
    
    authors = []
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
            defaults={'biography': author_data['biography']}
        )
        authors.append(author)
        if created:
            print(f"Created author: {author}")
    
    # Create sample books
    books_data = [
        {'title': 'Pride and Prejudice', 'author': authors[0], 'isbn': '9780141439518', 'genre': 'fiction'},
        {'title': '1984', 'author': authors[1], 'isbn': '9780451524935', 'genre': 'fiction'},
        {'title': 'Murder on the Orient Express', 'author': authors[2], 'isbn': '9780062693662', 'genre': 'fiction'},
    ]
    
    books = []
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            defaults={
                'author': book_data['author'],
                'isbn': book_data['isbn'],
                'genre': book_data['genre'],
                'available_copies': 3
            }
        )
        books.append(book)
        if created:
            print(f"Created book: {book}")
    
    # Create sample users and members
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com'},
        {'username': 'jane_smith', 'email': 'jane@example.com'},
        {'username': 'bob_wilson', 'email': 'bob@example.com'},
        {'username': 'alice_brown', 'email': 'alice@example.com'},
        {'username': 'charlie_davis', 'email': 'charlie@example.com'},
    ]
    
    members = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'email': user_data['email']}
        )
        member, created = Member.objects.get_or_create(user=user)
        members.append(member)
        if created:
            print(f"Created member: {member}")
    
    # Create sample loans (some active, some overdue)
    loans_data = [
        {'member': members[0], 'book': books[0], 'days_ago': 5, 'is_returned': False},  # Active
        {'member': members[1], 'book': books[1], 'days_ago': 20, 'is_returned': False},  # Overdue
        {'member': members[2], 'book': books[2], 'days_ago': 10, 'is_returned': True},   # Returned
        {'member': members[3], 'book': books[0], 'days_ago': 18, 'is_returned': False},  # Overdue
        {'member': members[4], 'book': books[1], 'days_ago': 3, 'is_returned': False},   # Active
    ]
    
    for loan_data in loans_data:
        loan_date = date.today() - timedelta(days=loan_data['days_ago'])
        due_date = loan_date + timedelta(days=14)
        
        loan, created = Loan.objects.get_or_create(
            member=loan_data['member'],
            book=loan_data['book'],
            is_returned=loan_data['is_returned'],
            defaults={
                'loan_date': loan_date,
                'due_date': due_date,
                'return_date': loan_date + timedelta(days=7) if loan_data['is_returned'] else None
            }
        )
        if created:
            status = "overdue" if due_date < date.today() and not loan.is_returned else "active" if not loan.is_returned else "returned"
            print(f"Created {status} loan: {loan}")
    
    print("Database seeding completed!")

if __name__ == '__main__':
    seed_database()
