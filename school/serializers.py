from rest_framework import serializers
from .models import School, Teacher, Subject, Level, Student, Staff


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'email', 'image', 'city', 'established_date', 'slogan']


class SchoolRequiredFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'school', 'name', 'qualification', 'date_of_birth', 'address', 'subject', 'joined_date']


class TeacherListSerializer(serializers.ModelSerializer):
    school = SchoolRequiredFieldSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'school', 'name', 'qualification', 'date_of_birth', 'address', 'subject', 'joined_date']


class LevelSerializer(serializers.ModelSerializer):
    school = SchoolRequiredFieldSerializer()

    class Meta:
        model = Level
        fields = ['id', 'school', 'level_name', 'student_number']


class LevelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['level_name', 'student_number']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'school', 'name', 'photo', 'gender', 'admission_date', 'level', 'date_of_birth', 'address',
                  'father_name',
                  'mother_name', 'guardian_name', 'parent_mobile_number', 'parent_telephone_number']


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'photo', 'gender', 'admission_date', 'level', 'date_of_birth', 'address', 'father_name',
                  'mother_name', 'guardian_name', 'parent_mobile_number', 'parent_telephone_number']


class StudentListSerializer(serializers.ModelSerializer):
    level = LevelUpdateSerializer()
    school = SchoolRequiredFieldSerializer()

    class Meta:
        model = Student
        fields = ['id', 'school', 'name', 'photo', 'gender', 'admission_date', 'level', 'date_of_birth', 'address',
                  'father_name',
                  'mother_name', 'guardian_name', 'parent_mobile_number', 'parent_telephone_number']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ['school']


class SubjectListSerializer(serializers.ModelSerializer):
    school = SchoolRequiredFieldSerializer()
    level = LevelUpdateSerializer()

    class Meta:
        model = Subject
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Staff


class StaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        exclude = ['school']


class StaffListSerializer(serializers.ModelSerializer):
    school = SchoolRequiredFieldSerializer()

    class Meta:
        model = Staff
        fields = '__all__'
