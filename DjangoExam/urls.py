"""DjangoExam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from exam import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index),  # 默认访问首页
    path('index/', views.index, name='index'),
    path('studentLogin/', views.studentlogin, name='studentLogin'),  # 学生登录
    path('startExam/', views.startExam, name='startExam'),  # 开始考试
    path('calculateGrade/', views.calculateGrade, name='calculateGrade'),  # 考试评分
    path('stulogout/', views.stulogout, name='stulogout'),  # 学生退出登录
    path('userfile/', views.userfile, name='userfile'),  # 个人信息
    path('examinfo/', views.examinfo, name='examinfo'),  # 考试信息
    # 角色登录
    path('admin_login/', views.admin_login, name='admin_login'),  # 管理员登录
    path('staff_login/', views.staff_login, name='staff_login'),  # 教务人员登录
    path('teacher_login/', views.teacher_login, name='teacher_login'),  # 教师登录
    path('logout_view/', views.logout_view, name='logout_view'),  # 退出
    # 仪表盘
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("academic_staff_dashboard/", views.academic_staff_dashboard, name="academic_staff_dashboard"),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    # 教师
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('create_exam/', views.create_exam, name='create_exam'),
    path('maintain_questions/', views.maintain_questions, name='maintain_questions'),
    path('maintain_questions/<int:paper_id>/', views.maintain_questions, name='maintain_questions'),
    path('maintain_papers/', views.maintain_papers, name='maintain_papers'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_question/<int:paper_id>/', views.add_question, name='add_question'),
    path('distribute_exam/<int:paper_id>/', views.distribute_exam, name='distribute_exam'),

    # 教务人员
    path('manage_academies/', views.manage_academies, name='manage_academies'),
    path('manage_academies/<int:academy_id>/', views.manage_academies, name='manage_academies'),
    path('delete_academy/<int:academy_id>/', views.manage_academies, name='delete_academy'),
    path('manage_majors/', views.manage_majors, name='manage_majors'),
    path('delete_major/<int:major_id>/', views.manage_majors, name='delete_major'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('manage_courses/<int:course_id>/', views.manage_courses, name='manage_courses_with_id'),
    path('delete_course/<int:course_id>/', views.manage_courses, name='delete_course'),
    path('manage_students/', views.manage_students, name='manage_students'),
    path('delete_student/<str:student_id>/', views.manage_students, name='delete_student'),
    path('edit_student/<str:student_id>/', views.manage_students, name='edit_student'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # 管理员
    path('admin_change/', views.admin_change, name='admin_change'),
    path('delete_teacher/<int:teacher_id>/', views.admin_change, name='delete_teacher'),
    path('delete_staff/<int:staff_id>/', views.admin_change, name='delete_staff'),
]
