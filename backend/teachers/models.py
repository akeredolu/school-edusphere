from django.db import models

class TeacherProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='teachers/photos/')
