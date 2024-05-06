import time
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.signals import Signal

from companyapi.settings import MAX_STUDENTS
from .models import Company, Student
from .utils import get_current_count

company_created = Signal()

@receiver(post_save, sender=Company)
def company_created_handler(sender, instance, created, **kwargs):
    if created:
        total_companies = Company.objects.count()
        if total_companies == 20:
            company_created.send(sender=Company, total_companies=total_companies)



@receiver(company_created)
def handle_company_created(sender, total_companies, **kwargs):
    # Handle the signal here
    print(f"Total companies in the database: {total_companies}. Database is full.")


# @receiver(pre_save, sender=Student)
# def pre_save_student(sender, instance, **kwargs):
#     # Count the number of students in the database
#     student_count = Student.objects.count()

#     # Check if the number of students is less than 20
#     if student_count >= 8:
#         # Cancel the save operation if the limit is reached
#         raise ValueError("Cannot save student. Maximum limit reached.")

@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, **kwargs):
    # time.sleep(10)
    if created:
        # Count the number of vacant seats
        curr_count = get_current_count()
        if curr_count<MAX_STUDENTS:
            # Print a message indicating the count of vacant seats
            print(f"Count of vacant seats: {MAX_STUDENTS-curr_count}")

