from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Student(models.Model):
    student_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    field_of_study = models.CharField(max_length=100)
    gpa = models.FloatField()
    password = models.CharField(max_length=128, default='student123')

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
