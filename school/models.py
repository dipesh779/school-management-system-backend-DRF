from django.db import models

GENDER = (
    ('male', 'male'),
    ('female', 'female')
)


class TimeStamp(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class School(TimeStamp):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/user', null=True, blank=True)
    established_date = models.DateField()
    slogan = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Teacher(TimeStamp):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    qualification = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, blank=True, null=True)
    joined_date = models.DateField()

    def __str__(self):
        return self.name


class Level(TimeStamp):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    level_name = models.CharField(max_length=100)
    student_number = models.IntegerField()

    def __str__(self):
        return self.level_name


class Student(TimeStamp):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="media/student")
    gender = models.CharField(max_length=100, choices=GENDER)
    admission_date = models.DateField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    parent_mobile_number = models.BigIntegerField()
    parent_telephone_number = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(TimeStamp):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Staff(TimeStamp):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER)
    address = models.CharField(max_length=100)
    joined_date = models.DateField(blank=True, null=True)
    phone_number = models.BigIntegerField()