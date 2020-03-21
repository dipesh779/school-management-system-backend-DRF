from django.urls import path
from .views import SchoolCreateView, SchoolDetailView, TeacherCreateView, \
    TeacherDetailView, LevelCreateView, LevelDetailView, StudentCreateView, \
    StudentDetailView, SubjectCreateView, SubjectDetailView, StaffCreateView, StaffDetailView

urlpatterns = [
    path('school', SchoolCreateView.as_view(), ),
    path('school/<int:pk>', SchoolDetailView.as_view(), ),

    path('teacher', TeacherCreateView.as_view(), ),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), ),

    path('level', LevelCreateView.as_view(), ),
    path('level/<int:pk>', LevelDetailView.as_view(), ),

    path('student', StudentCreateView.as_view(), ),
    path('student/<int:pk>', StudentDetailView.as_view(), ),

    path('subject', SubjectCreateView.as_view(), ),
    path('subject/<int:pk>', SubjectDetailView.as_view(), ),

    path('staff', StaffCreateView.as_view(),),
    path('staff/<int:pk>', StaffDetailView.as_view())

]
