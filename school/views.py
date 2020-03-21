from django.shortcuts import render
from user.token_helper import token_helper
from .models import School, Teacher, Level, Student, Subject, Staff
from .serializers import SchoolSerializer, TeacherSerializer, LevelSerializer, LevelUpdateSerializer, \
    StudentSerializer, StudentListSerializer, StudentUpdateSerializer, SubjectSerializer, SubjectListSerializer, \
    SubjectUpdateSerializer, TeacherListSerializer, StaffListSerializer, StaffUpdateSerializer, StaffSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SchoolCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser, ]
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        school = School.objects.all()
        serializer = SchoolSerializer(school, many=True)
        return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})


class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser, ]
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

    def get(self, request, pk):
        school = School.objects.get(pk=pk)
        serializer = SchoolSerializer(school)
        return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})

    def update(self, request, pk):
        school = School.objects.get(pk=pk)
        serializer = SchoolSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})
        else:
            return Response({'response': serializer.errors, 'status': status.HTTP_200_OK, })

    def delete(self, request, pk):
        serializer = School.objects.get(pk=pk)
        serializer.delete()
        return Response({'response': 'deleted', 'status': status.HTTP_200_OK})


class TeacherCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SchoolSerializer
    queryset = Teacher.objects.all()

    def get(self, request):
        school = token_helper(request)
        if school is not None:
            school = Teacher.objects.filter(school=school)
            serializer = TeacherListSerializer(school, many=True)
            return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})
        else:
            return Response({'message': 'school does not exist', 'status': status.HTTP_404_NOT_FOUND})

    def post(self, request):
        school = token_helper(request)
        if school is not None:
            request.data['school'] = school.id
            serializer = TeacherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'response': serializer.errors, 'status': status.HTTP_200_OK})


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get(self, request, pk):
        school = token_helper(request)
        teacher = Teacher.objects.get(pk=pk)
        if teacher.school == school:
            serializer = TeacherListSerializer(teacher)
            return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})

    def update(self, request, pk):
        school = token_helper(request)
        teacher = Teacher.objects.get(pk=pk)
        if teacher.school == school:
            serializer = TeacherSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'success', 'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'response': serializer.errors, 'status': status.HTTP_200_OK})

    def delete(self, request, pk):
        try:
            school = token_helper(request)
            teacher = Teacher.objects.get(pk=pk)
            if teacher.school == school:
                teacher.delete()
                return Response({'response': 'success', 'status': status.HTTP_200_OK})
            else:
                return Response({'response': 'error', 'status': status.HTTP_404_NOT_FOUND})
        except:
            return Response({'response': "teacher doesn't exist", 'status': status.HTTP_404_NOT_FOUND})


class LevelCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LevelSerializer
    queryset = Level.objects.all()

    def post(self, request):
        school = token_helper(request)
        if school is not None:
            request.data['school'] = school.id
            serializer = LevelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})

    def get(self, request, *args, **kwargs):
        school = token_helper(request)
        if school is not None:
            level = Level.objects.all()
            serializer = LevelSerializer(level, many=True)
            return Response({'status': status.HTTP_200_OK, 'response': serializer.data})


class LevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LevelSerializer
    queryset = Level.objects.all()

    def get(self, request, pk):
        try:
            school = token_helper(request)
            level = Level.objects.get(pk=pk)
            if level.school == school:
                serializer = LevelSerializer(level)
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "level doesn't exist"})

    def update(self, request, pk):
        try:
            school = token_helper(request)
            level = Level.objects.get(pk=pk)
            if level.school == school:
                serializer = LevelUpdateSerializer(level, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "data not found"})

    def delete(self, request, pk):
        try:
            school = token_helper(request)
            level = Level.objects.get(pk=pk)
            if level.school == school:
                level.delete()
                return Response({'status': status.HTTP_200_OK, 'response': 'delete success'})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "data doesn't exist"})


class StudentCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Student.objects.all()

    def get(self, request):
        school = token_helper(request)
        if school is not None:
            student = Student.objects.all()
            serializer = StudentListSerializer(student, many=True)
            return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "school doesn't exist"})

    def post(self, request):
        school = token_helper(request)
        request.data['school'] = school.id
        if school is not None:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "school doesn't exist"})


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Student.objects.all()

    def get(self, request, pk):
        try:
            school = token_helper(request)
            student = Student.objects.get(pk=pk)
            if student.school == school:
                serializer = StudentListSerializer(student)
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': 'student DoesNot exist'})

    def update(self, request, pk):
        try:
            school = token_helper(request)
            student = Student.objects.get(pk=pk)
            if student.school == school:
                serializer = StudentUpdateSerializer(student, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': 'student DoesNot exist'})

    def delete(self, request, pk):
        try:
            school = token_helper(request)
            student = Student.objects.get(pk=pk)
            if student.school == school:
                student.delete()
                return Response({'status': status.HTTP_200_OK, 'response': 'delete success'})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': 'student DoesNot exist'})


class SubjectCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Subject.objects.all()

    def get(self, request):
        school = token_helper(request)
        if school is not None:
            subject = Subject.objects.all()
            serializer = SubjectListSerializer(subject, many=True)
            return Response({'status': status.HTTP_200_OK, 'response': serializer.data})

    def post(self, request):
        school = token_helper(request)
        if school is not None:
            request.data['school'] = school.id
            serializer = SubjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Subject.objects.all()

    def get(self, request, pk):
        try:
            school = token_helper(request)
            subject = Subject.objects.get(pk=pk)
            if subject.school == school:
                serializer = SubjectListSerializer(subject)
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "subject doesn't exist"})

    def update(self, request, pk):
        try:
            school = token_helper(request)
            subject = Subject.objects.get(pk=pk)
            if subject.school == school:
                serializer = SubjectUpdateSerializer(subject, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})

        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "subject doesn't exist"})

    def delete(self, request, pk):
        try:
            school = token_helper(request)
            subject = Subject.objects.get(pk=pk)
            if subject.school == school:
                subject.delete()
                return Response({'status': status.HTTP_200_OK, 'response': 'delete success'})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})

        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "subject doesn't exist"})


class StaffCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Staff.objects.all()

    def get(self, request):
        school = token_helper(request)
        if school is not None:
            staff = Staff.objects.all()
            serializer = StaffListSerializer(staff, many=True)
            return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})

    def post(self, request):
        school = token_helper(request)
        if school is not None:
            request.data['school'] = school.id
            serializer = StaffSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Staff.objects.all()

    def get(self, request, pk):
        try:
            school = token_helper(request)
            staff = Staff.objects.get(pk=pk)
            if staff.school == school:
                serializer = StaffListSerializer(staff)
                return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "staff doesn't exist"})

    def update(self, request, pk):
        try:
            school = token_helper(request)
            staff = Staff.objects.get(pk=pk)
            if staff.school == school:
                serializer = StaffUpdateSerializer(staff, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK, 'response': serializer.data})
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'response': serializer.errors})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})

        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "staff doesn't exist"})

    def delete(self, request, pk):
        try:
            school = token_helper(request)
            staff = Staff.objects.get(pk=pk)
            if staff.school == school:
                staff.delete()
                return Response({'status': status.HTTP_200_OK, 'response': 'delete success'})
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'response': 'unauthorized'})

        except:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'response': "staff doesn't exist"})