from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='students/photos/')

