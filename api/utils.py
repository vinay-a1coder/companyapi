from .models import Student

def get_current_count():
    count = Student.objects.count()
    return count