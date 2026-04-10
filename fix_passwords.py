import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'students.settings')
django.setup()

from students.models import Student

# Fix all existing students' passwords
students = Student.objects.all()
for student in students:
    student.set_password('student123')
    student.save()
    print(f"Fixed password for {student.first_name} {student.last_name}")

print(f"\nTotal students updated: {students.count()}")
