from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from .models import Student
from .forms import StudentForm


# Create your views here.
def index(request):
  return render(request, 'students/index.html', {
    'students': Student.objects.all()
  })


def view_student(request, id):
  return HttpResponseRedirect(reverse('index'))


def add(request):
  if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
      new_student_number = form.cleaned_data['student_number']
      new_first_name = form.cleaned_data['first_name']
      new_last_name = form.cleaned_data['last_name']
      new_email = form.cleaned_data['email']
      new_field_of_study = form.cleaned_data['field_of_study']
      new_gpa = form.cleaned_data['gpa']

      new_student = Student(
        student_number=new_student_number,
        first_name=new_first_name,
        last_name=new_last_name,
        email=new_email,
        field_of_study=new_field_of_study,
        gpa=new_gpa
      )
      new_student.set_password('student123')  # Hash the default password
      new_student.save()
      
      # Send email notification
      try:
        login_url = request.build_absolute_uri(reverse('student_login'))
        send_mail(
          subject='Welcome to Student Management System',
          message=f'Hello {new_first_name} {new_last_name},\n\nYou have been successfully registered in our system.\n\nStudent Number: {new_student_number}\nField of Study: {new_field_of_study}\nGPA: {new_gpa}\n\nYour Login Credentials:\nStudent Number: {new_student_number}\nPassword: student123\n\nAccess your student portal here:\n{login_url}\n\nBest regards,\nGodwin\'s Palace Academy',
          from_email=settings.DEFAULT_FROM_EMAIL,
          recipient_list=[new_email],
          fail_silently=False,
        )
      except Exception as e:
        print(f"Email sending failed: {e}")
      
      return render(request, 'students/add.html', {
        'form': StudentForm(),
        'success': True
      })
  else:
    form = StudentForm()
  return render(request, 'students/add.html', {
    'form': StudentForm()
  })


def edit(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      
      # Send email notification
      try:
        login_url = request.build_absolute_uri(reverse('student_login'))
        send_mail(
          subject='Your Student Record Has Been Updated',
          message=f'Hello {student.first_name} {student.last_name},\n\nYour student record has been updated.\n\nStudent Number: {student.student_number}\nField of Study: {student.field_of_study}\nGPA: {student.gpa}\n\nView your updated information:\n{login_url}\n\nBest regards,\nGodwin\'s Palace Academy',
          from_email=settings.DEFAULT_FROM_EMAIL,
          recipient_list=[student.email],
          fail_silently=False,
        )
      except Exception as e:
        print(f"Email sending failed: {e}")
      
      return render(request, 'students/edit.html', {
        'form': form,
        'success': True
      })
  else:
    student = Student.objects.get(pk=id)
    form = StudentForm(instance=student)
  return render(request, 'students/edit.html', {
    'form': form
  })


def delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    student_email = student.email
    student_name = f"{student.first_name} {student.last_name}"
    
    # Send email notification before deleting
    try:
      send_mail(
        subject='Your Student Record Has Been Removed',
        message=f'Hello {student_name},\n\nYour student record has been removed from our system.\n\nIf you have any questions, please contact the administration.\n\nBest regards,\nGodwin\'s Palace Academy',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student_email],
        fail_silently=False,
      )
    except Exception as e:
      print(f"Email sending failed: {e}")
    
    student.delete()
  return HttpResponseRedirect(reverse('index'))



def student_login(request):
  if request.method == 'POST':
    student_number = request.POST.get('student_number')
    password = request.POST.get('password')
    
    try:
      student = Student.objects.get(student_number=student_number)
      if student.check_password(password):
        request.session['student_id'] = student.id
        return HttpResponseRedirect(reverse('student_dashboard'))
      else:
        return render(request, 'students/student_login.html', {
          'error': 'Invalid student number or password'
        })
    except Student.DoesNotExist:
      return render(request, 'students/student_login.html', {
        'error': 'Invalid student number or password'
      })
  
  return render(request, 'students/student_login.html')


def student_dashboard(request):
  student_id = request.session.get('student_id')
  if not student_id:
    return HttpResponseRedirect(reverse('student_login'))
  
  try:
    student = Student.objects.get(id=student_id)
    return render(request, 'students/student_dashboard.html', {
      'student': student
    })
  except Student.DoesNotExist:
    return HttpResponseRedirect(reverse('student_login'))


def student_logout(request):
  if 'student_id' in request.session:
    del request.session['student_id']
  return HttpResponseRedirect(reverse('student_login'))
