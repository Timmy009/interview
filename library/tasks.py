from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import date

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    """
    Daily task to check for overdue book loans and send email notifications.
    """
    today = date.today()
    overdue_loans = Loan.objects.filter(
        is_returned=False,
        due_date__lt=today
    ).select_related('member__user', 'book')
    
    for loan in overdue_loans:
        try:
            member_email = loan.member.user.email
            book_title = loan.book.title
            days_overdue = (today - loan.due_date).days
            
            send_mail(
                subject='Overdue Book Reminder',
                message=f'Hello {loan.member.user.username},\n\n'
                       f'Your book "{book_title}" is {days_overdue} days overdue.\n'
                       f'Please return it as soon as possible to avoid late fees.\n\n'
                       f'Due date was: {loan.due_date}\n'
                       f'Thank you.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )
        except Exception as e:
            # Log error but continue processing other loans
            print(f"Failed to send overdue notification for loan {loan.id}: {e}")
    
    return f"Processed {overdue_loans.count()} overdue loans"
