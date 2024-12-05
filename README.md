<!-- PROJECT LOGO -->
<div align="center">
    <img src="https://github.com/user-attachments/assets/c56ec18e-af4d-42a2-8def-772cbefbb604" alt="logoText">
    <h3>HR Management System READ ME</h3>
</div>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#gant-chart">Gant Chart</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

The HR Management System is a comprehensive platform designed to streamline and optimize the core functions of Human Resources. Built to simplify processes like employee data management, attendance tracking, payroll processing, performance evaluations, and recruitment, this system serves as an all-in-one solution for HR departments of any size. By centralizing data and automating repetitive tasks, it reduces administrative workload and helps HR teams focus on strategic activities, such as talent development and employee engagement.

Key features include:

- Employee Profiles: Centralized database for managing employee records and personal information. Automated Password generation sent through email.
- Attendance Tracking: Efficient tracking of attendance, leave, and absences, providing transparency and accountability.
- Payroll Management: Salary calculations, deductions, and payments with secure storage and accessibility and downloadable pdf paylisp.
- Performance Feedback: Tools to facilitate continuous performance tracking, sanctions, self assessment and reviews.
- Recruitment: Simplifies the hiring process with applicant tracking, resume management, job openings and posting, and interviews .

#Reminders
--Don't use previous project
--Commit through branch

#StartUP
---IN VSCode Powershell / Cmd 1. direct to your folder 2. Make sure virtual environment is installed
python -m pip install virtualenv
py -m pip install virtualenv 3. Create the environment
virtualenv myenv 4. Activate
VS Code : myenv\Scripts\activate (mas better for github purposes)
cmd: .\myenv\Scripts\activate 5. Should have (myenv) on the left side 6. Install Django
pip install django 7. Create Project
django-admin startproject projectname 8. Create app
cd projectname
django-adin startapp appname 9. Continuation through .py files
!!! Make sure to check directories and file arrangements

#UI
CSS Framework: Tailwind CSS
##Installation Instructions 1. In settings.py, INSTALLED_APPS - add 'tailwind', 2. In Powershell (myenv) - python -m pip install django-tailwind - cd to project then python manage.py tailwind init - app_name[theme]? type "theme" - add 'theme' and django_browser_reload on INSTALLED_APPS in setting.py - pip install django-browser-reload 3. Settings.py - Add code line TAILWIND_APP_NAME = 'theme' - Add INTERNAL_IPS = ["127.0.0.1",] 4. MIDDLEWARE
-add to the last "django_browser_reload.middleware.BrowserReloadMiddleware", 5. In projects urls.py
-add path("**reload**/", include("django_browser_reload.urls")), 6. python managge.py tailwind start

https://www.youtube.com/watch?v=GepQBpHNgrk

#DATABASE
---POSTGRESQL
Installations 1. Download Postgresql .exe https://www.postgresql.org/ftp/pgadmin/pgadmin4/v8.12/windows/ 2. Install Necessary, pgAdmin 3. Create the Database through pgAdmin, name it dbhrmanagement, Just check my files sa database sa settings (Right click in pgAdmin to execute commands) - General Tab then Owner is Postgres - Definition
Econding - UTF8
Tablespace -pd_default
Collation and Character - english / en_US/ - Security - Privileges - Grantee fyang - else ALL 4. create your models, modify setting.py

#Gant Chart
https://docs.google.com/spreadsheets/d/100kTUpP4Sychp47k7l7S2iiFd9uNb3wG9xwUYE7GOIQ/edit?gid=0#gid=0




