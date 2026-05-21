# DjangoExam 在线考试管理系统

基于 Django 3.2 的课程考试系统，包含学生端考试、教师组卷、教务管理与管理员管理功能。

## 功能概览

- 学生端：登录、查看可参加试卷、参加考试、自动判分、查看成绩、查看个人信息
- 教师端：登录、教师主页、创建试卷、维护试卷与试题、发布考试（流程入口）
- 教务端：登录、学院/专业/课程/学生信息管理（增删改）
- 管理员端：登录、教师与教务人员管理（增删改）

## 技术栈

- Python 3.x
- Django 3.2.x
- MySQL
- django-simpleui（Django Admin 美化）

## 项目结构

```text
DjangoExam/
├── DjangoExam/                # 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── exam/                      # 业务应用
│   ├── models.py              # 学院/专业/课程/学生/题库/试卷/成绩/角色模型
│   ├── views.py               # 学生、教师、教务、管理员业务逻辑
│   ├── urls.py
│   └── migrations/
├── templates/                 # 页面模板
│   ├── index.html
│   ├── login.html
│   ├── adminLogin.html
│   ├── staffLogin.html
│   ├── teacherLogin.html
│   └── ...
├── static/                    # 静态资源（含 bootstrap 资源）
├── artifacts/                 # 页面截图
├── manage.py
└── README.md
```

## 快速开始

1. 克隆并进入项目目录

```bash
git clone https://github.com/youngxx423/DjangoExam.git
cd DjangoExam
```

2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install django==3.2.19 django-simpleui mysqlclient
```

3. 配置数据库（`DjangoExam/settings.py`）

默认配置为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exam',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306
    }
}
```

请先在 MySQL 中创建数据库 `exam`，并按实际环境修改账号密码。

4. 迁移数据库并启动

```bash
python manage.py migrate
python manage.py runserver
```

浏览器访问：`http://127.0.0.1:8000/`

## 主要访问路径

- `/`：系统首页
- `/studentLogin/`：学生登录
- `/admin_login/`：管理员登录
- `/staff_login/`：教务登录
- `/teacher_login/`：教师登录
- `/admin/`：Django 后台管理

## 核心数据模型

- `Academy`：学院
- `Major`：专业
- `Course`：课程
- `Student`：学生
- `QuestionBank`：题库
- `TestPaper`：试卷
- `Record`：成绩记录
- `AdminManager` / `AcademicStaff` / `Teacher`：三类角色账号
- `Exam`：考试（扩展模型）

## 使用说明

- 首次使用建议先进入 `/admin/` 录入基础数据（学院、专业、课程、角色账号、学生、题库与试卷）。
- 系统当前采用数据库明文密码字段用于演示教学流程，不建议直接用于生产环境。

## 页面预览

- 首页：`artifacts/01_home.png`
- 学生登录：`artifacts/02_student_login.png`
- 管理员登录：`artifacts/05_admin_login.png`
- 教务登录：`artifacts/06_staff_login.png`
- 教师登录：`artifacts/07_teacher_login.png`
