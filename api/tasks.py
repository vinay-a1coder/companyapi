from celery import Celery, shared_task
from .models import Student, Email
import random
import logging
import time
from companyapi.celery import app
logger = logging.getLogger(__name__)


# @shared_task
# def generate_random_message(id):
#     try:
#         # You may fetch the student object using the student_id if required
#         # For simplicity, we are generating a random message here
#         breakpoint()
#         messages = [
#             "Hello! How are you today?",
#             "Hi, have a great day!",
#             "Hey, what's up?",
#         ]
#         message = random.choice(messages)
#         # Create and save Email instance
#         Email.objects.create(to="test@example.com", desc=message)
#     except Exception as e:
#         print("An error occurred in generate_random_message task:", e)


@app.task
def generate_random_message(student_id):
    try:
        # breakpoint()
        student = Student.objects.get(pk=student_id)
        messages = [
            "Hello! How are you today?",
            "Hi, have a great day!",
            "Hey, what's up?",
        ]
        message = random.choice(messages)
        # print(message)
        # time.sleep(10)
        # Create and save Email instance
        Email.objects.create(to=student.email, desc=message)
    except Student.DoesNotExist:
        logger.error("Student with ID %s does not exist", student_id)
    except Exception as e:
        logger.exception("An error occurred in generate_random_message task: %s", e)

    