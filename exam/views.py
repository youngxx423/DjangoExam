from datetime import datetime

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from exam import models
from exam.models import (
    AcademicStaff,
    Academy,
    AdminManager,
    Course,
    Major,
    QuestionBank,
    Student,
    Teacher,
    TestPaper,
)


def _session_user(request):
    if not request.session.get("is_login"):
        return None, None
    return request.session.get("username"), request.session.get("role")


# 学生登录
def studentlogin(request):
    if request.method == "POST":
        sid = request.POST.get("sid", "").strip()
        password = request.POST.get("password", "")
        student = Student.objects.filter(sid=sid).first()
        if not student:
            return render(request, "login.html", {"message": "学号不存在"})
        if password != student.pwd:
            return render(request, "login.html", {"message": "密码不正确"})

        request.session["username"] = sid
        request.session["is_login"] = True
        request.session["role"] = "student"
        paper = TestPaper.objects.filter(major=student.major)
        grade = models.Record.objects.filter(sid=student.sid)
        return render(request, "index.html", {"student": student, "paper": paper, "grade": grade})

    if request.method == "GET":
        return render(request, "login.html")
    return HttpResponse("请使用GET或POST请求数据")


# 首页
def index(request):
    username, role = _session_user(request)
    if role == "student" and username:
        student = Student.objects.filter(sid=username).first()
        if student:
            paper = TestPaper.objects.filter(major=student.major)
            return render(request, "index.html", {"student": student, "paper": paper})
        return render(request, "index.html", {"error_message": "找不到匹配的学生记录"})
    return render(request, "index.html")


def userfile(request):
    username, role = _session_user(request)
    if role != "student" or not username:
        return redirect("studentLogin")
    student = Student.objects.filter(sid=username).first()
    if not student:
        return redirect("studentLogin")
    return render(request, "userfile.html", {"student": student})


# 学生退出登录
def stulogout(request):
    request.session.clear()
    return redirect(reverse("index"))


# 开始考试
def startExam(request):
    username, role = _session_user(request)
    sid = username if role == "student" and username else request.GET.get("sid")
    title = request.GET.get("title", "")
    subject = request.GET.get("subject", "")

    student = Student.objects.filter(sid=sid).first()
    if not student:
        return HttpResponse("Student does not exist.")

    paper = TestPaper.objects.filter(title=title, course__course_name=subject, major=student.major)
    if not paper.exists():
        return HttpResponse("未找到对应试卷。")

    context = {
        "student": student,
        "paper": paper,
        "title": title,
        "subject": subject,
        "count": paper.count(),
    }
    return render(request, "exam.html", context=context)


def examinfo(request):
    username, role = _session_user(request)
    if role != "student" or not username:
        return render(request, "examinfo.html")

    student = Student.objects.filter(sid=username).first()
    if not student:
        return render(request, "examinfo.html")
    grade = models.Record.objects.filter(sid=student.sid)
    return render(request, "examinfo.html", {"student": student, "grade": grade})


# 计算考试成绩
def calculateGrade(request):
    if request.method != "POST":
        return redirect("index")

    username, role = _session_user(request)
    sid = username if role == "student" and username else request.POST.get("sid")
    subject = request.POST.get("subject")

    student = Student.objects.filter(sid=sid).first()
    if not student:
        return redirect("studentLogin")

    course = Course.objects.filter(course_name=subject).first()
    if not course:
        return HttpResponse("考试科目不存在。")

    papers = TestPaper.objects.filter(major=student.major, course=course)
    questions = QuestionBank.objects.filter(testpaper__in=papers).distinct()

    stu_grade = 0
    for question in questions:
        stu_ans = request.POST.get(str(question.id))
        if stu_ans == question.answer:
            stu_grade += question.score

    models.Record.objects.create(
        sid_id=student.sid,
        course_id=course.id,
        grade=stu_grade,
        rtime=datetime.now(),
    )

    paper = TestPaper.objects.filter(major=student.major)
    grade = models.Record.objects.filter(sid=student.sid)
    return render(request, "index.html", {"student": student, "paper": paper, "grade": grade, "score": stu_grade})


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        admin_manager = AdminManager.objects.filter(username=username).first()
        if not admin_manager:
            return render(request, "adminLogin.html", {"message": "管理员不存在"})
        if password != admin_manager.password:
            return render(request, "adminLogin.html", {"message": "密码不正确"})

        request.session["username"] = username
        request.session["is_login"] = True
        request.session["role"] = "admin"
        return redirect("admin_dashboard")

    if request.method == "GET":
        return render(request, "adminLogin.html")
    return HttpResponse("请使用GET或POST请求数据")


def staff_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        academic_staff = AcademicStaff.objects.filter(username=username).first()
        if not academic_staff:
            return render(request, "staffLogin.html", {"message": "教务人员不存在"})
        if password != academic_staff.password:
            return render(request, "staffLogin.html", {"message": "密码不正确"})

        request.session["username"] = username
        request.session["is_login"] = True
        request.session["role"] = "academic_staff"
        return redirect("academic_staff_dashboard")

    if request.method == "GET":
        return render(request, "staffLogin.html")
    return HttpResponse("请使用GET或POST请求数据")


def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        teacher = Teacher.objects.filter(username=username).first()
        if not teacher:
            return render(request, "teacherLogin.html", {"message": "教师不存在"})
        if password != teacher.password:
            return render(request, "teacherLogin.html", {"message": "密码不正确"})

        request.session["username"] = username
        request.session["is_login"] = True
        request.session["role"] = "teacher"
        return redirect("teacher_dashboard")

    if request.method == "GET":
        return render(request, "teacherLogin.html")
    return HttpResponse("请使用GET或POST请求数据")


def logout_view(request):
    logout(request)
    request.session.clear()
    return redirect(reverse("index"))


def admin_dashboard(request):
    username, role = _session_user(request)
    if role != "admin" or not username:
        return redirect(reverse("index"))

    admin_manager = AdminManager.objects.filter(username=username).first()
    teachers = Teacher.objects.all()
    academic_staff = AcademicStaff.objects.all()
    return render(
        request,
        "admin_dashboard.html",
        {"admin_manager": admin_manager, "teachers": teachers, "academic_staff": academic_staff},
    )


def academic_staff_dashboard(request):
    username, role = _session_user(request)
    if role != "academic_staff" or not username:
        return redirect(reverse("index"))

    academic_staff = AcademicStaff.objects.filter(username=username).first()
    return render(request, "academic_staff_dashboard.html", {"academic_staff": academic_staff})


def teacher_dashboard(request):
    username, role = _session_user(request)
    if role != "teacher" or not username:
        return redirect(reverse("index"))

    teacher = Teacher.objects.filter(username=username).first()
    exams = TestPaper.objects.all()
    return render(request, "teacher_dashboard.html", {"teacher": teacher, "exams": exams})


def create_exam(request):
    username, role = _session_user(request)
    if role != "teacher" or not username:
        return redirect(reverse("index"))

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        course_id = request.POST.get("course")
        major_id = request.POST.get("major")
        questions_ids = request.POST.getlist("questions")
        time_limit = request.POST.get("time_limit")

        if not all([title, course_id, major_id, time_limit]):
            courses = Course.objects.all()
            majors = Major.objects.all()
            questions = QuestionBank.objects.all()
            return render(
                request,
                "create_exam.html",
                {"courses": courses, "majors": majors, "questions": questions, "message": "请填写完整信息"},
            )

        course = Course.objects.filter(id=course_id).first()
        major = Major.objects.filter(id=major_id).first()
        questions = QuestionBank.objects.filter(id__in=questions_ids)
        if not course or not major:
            return HttpResponse("课程或专业不存在")

        examtime = datetime.now()
        paper = TestPaper.objects.create(
            title=title,
            course=course,
            major=major,
            time=int(time_limit),
            examtime=examtime,
        )
        paper.pid.set(questions)
        return redirect("teacher_dashboard")

    courses = Course.objects.all()
    majors = Major.objects.all()
    questions = QuestionBank.objects.all()
    return render(request, "create_exam.html", {"courses": courses, "majors": majors, "questions": questions})


def teacher_profile(request):
    username, role = _session_user(request)
    if role != "teacher" or not username:
        return render(request, "index.html")
    teacher = Teacher.objects.filter(username=username).first()
    if not teacher:
        return render(request, "index.html")
    return render(request, "teacher_profile.html", {"teacher": teacher})


def maintain_papers(request):
    papers = TestPaper.objects.all()
    return render(request, "maintain_papers.html", {"papers": papers})


def maintain_questions(request, paper_id=None):
    if paper_id is None:
        papers = TestPaper.objects.all()
        return render(request, "maintain_papers.html", {"papers": papers})

    paper = TestPaper.objects.filter(id=paper_id).first()
    if not paper:
        return HttpResponse("试卷不存在")
    return render(request, "maintain_questions.html", {"paper": paper})


def add_question(request, paper_id=None):
    if request.method == "POST" and paper_id is not None:
        paper = TestPaper.objects.filter(id=paper_id).first()
        if not paper:
            return HttpResponse("试卷不存在")
        new_title = request.POST.get("new_title", "").strip()
        if new_title:
            question = QuestionBank.objects.create(
                major=paper.major,
                course=paper.course,
                title=new_title,
                qtype="单选",
                a="A",
                b="B",
                c="C",
                d="D",
                answer="A",
                difficulty="easy",
                score=2,
            )
            paper.pid.add(question)
            return redirect("maintain_questions", paper_id=paper.id)
    return render(request, "add_question.html", {"paper_id": paper_id})


def distribute_exam(request, paper_id):
    paper = TestPaper.objects.filter(id=paper_id).first()
    if not paper:
        return HttpResponse("试卷不存在")
    return redirect("teacher_dashboard")


def edit_profile(request):
    return render(request, "edit_profile.html")


def manage_academies(request, academy_id=None):
    if request.method == "GET" and request.resolver_match and request.resolver_match.url_name == "delete_academy":
        Academy.objects.filter(id=academy_id).delete()
        return redirect("manage_academies")

    if request.method == "POST":
        new_academy_name = request.POST.get("new_academy_name")
        if new_academy_name:
            Academy.objects.create(name=new_academy_name.strip())
            return redirect("manage_academies")

        academy_id = request.POST.get("academy_id")
        updated_academy_name = request.POST.get("updated_academy_name")
        if academy_id and updated_academy_name:
            academy = Academy.objects.filter(id=academy_id).first()
            if academy:
                academy.name = updated_academy_name.strip()
                academy.save()
            return redirect("manage_academies")

        deleted_academy_id = request.POST.get("deleted_academy_id")
        if deleted_academy_id:
            Academy.objects.filter(id=deleted_academy_id).delete()
            return redirect("manage_academies")

    academies = Academy.objects.all()
    return render(request, "manage_academies.html", {"academies": academies})


def manage_majors(request, major_id=None):
    if request.method == "GET" and request.resolver_match and request.resolver_match.url_name == "delete_major":
        Major.objects.filter(id=major_id).delete()
        return redirect("manage_majors")

    if request.method == "POST":
        new_major_name = request.POST.get("new_major_name")
        academy_id = request.POST.get("academy_id")
        if new_major_name and academy_id:
            academy = Academy.objects.filter(id=academy_id).first()
            if academy:
                Major.objects.create(major=new_major_name.strip(), academy=academy)
            return redirect("manage_majors")

        major_id = request.POST.get("major_id")
        updated_major_name = request.POST.get("updated_major_name")
        if major_id and updated_major_name:
            major = Major.objects.filter(id=major_id).first()
            if major:
                major.major = updated_major_name.strip()
                major.save()
            return redirect("manage_majors")

        deleted_major_id = request.POST.get("deleted_major_id")
        if deleted_major_id:
            Major.objects.filter(id=deleted_major_id).delete()
            return redirect("manage_majors")

    majors = Major.objects.select_related("academy").all()
    academies = Academy.objects.all()
    return render(request, "manage_majors.html", {"majors": majors, "academies": academies})


def manage_courses(request, course_id=None):
    if request.method == "GET" and request.resolver_match and request.resolver_match.url_name == "delete_course":
        Course.objects.filter(id=course_id).delete()
        return redirect("manage_courses")

    if request.method == "POST":
        new_course_name = request.POST.get("new_course_name")
        if new_course_name:
            Course.objects.create(course_id=f"C{int(datetime.now().timestamp())}", course_name=new_course_name.strip())
            return redirect("manage_courses")

        course_id = request.POST.get("course_id")
        updated_course_name = request.POST.get("updated_course_name")
        if course_id and updated_course_name:
            course = Course.objects.filter(id=course_id).first()
            if course:
                course.course_name = updated_course_name.strip()
                course.save()
            return redirect("manage_courses")

        deleted_course_id = request.POST.get("deleted_course_id")
        if deleted_course_id:
            Course.objects.filter(id=deleted_course_id).delete()
            return redirect("manage_courses")

    courses = Course.objects.all()
    return render(request, "manage_courses.html", {"courses": courses})


def manage_students(request, student_id=None):
    if request.method == "GET" and request.resolver_match and request.resolver_match.url_name == "delete_student":
        Student.objects.filter(sid=student_id).delete()
        return redirect("manage_students")

    if request.method == "POST":
        new_student_name = request.POST.get("new_student_name")
        if new_student_name:
            academy = Academy.objects.first()
            major = Major.objects.first()
            if not academy or not major:
                return HttpResponse("请先创建学院和专业")
            sid = f"S{int(datetime.now().timestamp())}"
            Student.objects.create(
                sid=sid,
                name=new_student_name.strip(),
                sex=True,
                age=18,
                academy=academy,
                major=major,
                sclass="Demo",
                email=f"{sid.lower()}@demo.local",
                pwd="123456",
            )
            return redirect("manage_students")

        student_sid = request.POST.get("student_id")
        updated_student_name = request.POST.get("updated_student_name")
        if student_sid and updated_student_name:
            student = Student.objects.filter(sid=student_sid).first()
            if student:
                student.name = updated_student_name.strip()
                student.save()
            return redirect("manage_students")

        deleted_student_sid = request.POST.get("deleted_student_id")
        if deleted_student_sid:
            Student.objects.filter(sid=deleted_student_sid).delete()
            return redirect("manage_students")

    students = Student.objects.all()
    return render(request, "manage_students.html", {"students": students})


def admin_change(request, teacher_id=None, staff_id=None):
    if request.method == "GET" and request.resolver_match:
        if request.resolver_match.url_name == "delete_teacher":
            Teacher.objects.filter(id=teacher_id).delete()
            return redirect("admin_change")
        if request.resolver_match.url_name == "delete_staff":
            AcademicStaff.objects.filter(id=staff_id).delete()
            return redirect("admin_change")

    if request.method == "POST":
        new_teacher_name = request.POST.get("new_teacher_name")
        if new_teacher_name:
            suffix = int(datetime.now().timestamp())
            Teacher.objects.create(
                username=f"teacher{suffix}",
                name=new_teacher_name.strip(),
                age=30,
                sex=True,
                password="123456",
                role="teacher",
            )
            return redirect("admin_change")

        teacher_id = request.POST.get("teacher_id")
        updated_teacher_name = request.POST.get("updated_teacher_name")
        if teacher_id and updated_teacher_name:
            teacher = Teacher.objects.filter(id=teacher_id).first()
            if teacher:
                teacher.name = updated_teacher_name.strip()
                teacher.save()
            return redirect("admin_change")

        deleted_teacher_id = request.POST.get("deleted_teacher_id")
        if deleted_teacher_id:
            Teacher.objects.filter(id=deleted_teacher_id).delete()
            return redirect("admin_change")

        new_staff_name = request.POST.get("new_staff_name")
        if new_staff_name:
            suffix = int(datetime.now().timestamp())
            AcademicStaff.objects.create(
                username=f"staff{suffix}",
                name=new_staff_name.strip(),
                age=30,
                sex=True,
                password="123456",
                role="academic_staff",
            )
            return redirect("admin_change")

        staff_id = request.POST.get("staff_id")
        updated_staff_name = request.POST.get("updated_staff_name")
        if staff_id and updated_staff_name:
            staff = AcademicStaff.objects.filter(id=staff_id).first()
            if staff:
                staff.name = updated_staff_name.strip()
                staff.save()
            return redirect("admin_change")

        deleted_staff_id = request.POST.get("deleted_staff_id")
        if deleted_staff_id:
            AcademicStaff.objects.filter(id=deleted_staff_id).delete()
            return redirect("admin_change")

    teachers = Teacher.objects.all()
    academic_staff = AcademicStaff.objects.all()
    return render(request, "admin_dashboard.html", {"teachers": teachers, "academic_staff": academic_staff})
