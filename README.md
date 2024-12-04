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
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

The HR Management System is a comprehensive platform designed to streamline and optimize the core functions of Human Resources. Built to simplify processes like employee data management, attendance tracking, payroll processing, performance evaluations, and recruitment, this system serves as an all-in-one solution for HR departments of any size. By centralizing data and automating repetitive tasks, it reduces administrative workload and helps HR teams focus on strategic activities, such as talent development and employee engagement.

Key features include:

- Employee Profiles: Centralized database for managing employee records and personal information.
- Attendance Tracking: Efficient tracking of attendance, leave, and absences, providing transparency and accountability.
- Payroll Management: Automated calculations, deductions, and payments with secure storage and accessibility
- Performance Feedback: Tools to facilitate continuous performance tracking, goal-setting, and reviews.
- Recruitment: Simplifies the hiring process with applicant tracking, resume management, and scheduling capabilities.
- Reporting and Analytics: Real-time insights into HR data to support decision-making and compliance.

#Reminders
--Don't use previous project
--Commit through branch


## Built With
The HR Management System is a comprehensive platform designed to streamline and optimize the core functions of Human Resources. Built to simplify processes like employee data management, attendance tracking, payroll processing, performance evaluations, and recruitment, this system serves as an all-in-one solution for HR departments of any size. By centralizing data and automating repetitive tasks, it reduces administrative workload and helps HR teams focus on strategic activities, such as talent development and employee engagement.

Key features include:

- Employee Profiles: Centralized database for managing employee records and personal information.
- Attendance Tracking: Efficient tracking of attendance, leave, and absences, providing transparency and accountability.
- Payroll Management: Automated calculations, deductions, and payments with secure storage and accessibility
- Performance Feedback: Tools to facilitate continuous performance tracking, goal-setting, and reviews.
- Recruitment: Simplifies the hiring process with applicant tracking, resume management, and scheduling capabilities.
- Reporting and Analytics: Real-time insights into HR data to support decision-making and compliance.

#Reminders
--Don't use previous project
--Commit through branch

## Getting Started

1. **Direct to your folder**
   - Open your terminal or command prompt.
   - Navigate to the folder where you want to set up your Django project.

2. **Ensure virtual environment is installed**
   - Run the following commands to install virtualenv if not already installed:
     ```bash
     python -m pip install virtualenv
     py -m pip install virtualenv
     ```

3. **Create the environment**
   - Run:
     ```bash
     virtualenv myenv
     ```

4. **Activate the environment**
   - For VS Code:
     ```bash
     myenv\Scripts\activate
     ```
   - For Command Prompt:
     ```bash
     .\myenv\Scripts\activate
     ```
   - You should see `(myenv)` on the left side of your terminal prompt.

5. **Install Django**
   - Run:
     ```bash
     pip install django
     ```

6. **Create the project**
   - Run:
     ```bash
     django-admin startproject projectname
     ```

7. **Create an app**
   - Navigate to your project directory:
     ```bash
     cd projectname
     ```
   - Create a new app:
     ```bash
     django-admin startapp appname
     ```

8. **Ensure proper file arrangement**
   - Verify your directories and files are correctly set up.
   - Continuation of the setup involves editing `.py` files as needed for your project.

# Tailwind CSS Framework Setup

## Installation Instructions

1. **Modify `INSTALLED_APPS` in `settings.py`**
   - Add `'tailwind'` to the list of installed apps.

2. **Install dependencies and initialize Tailwind**
   - In Powershell (inside the virtual environment `myenv`), run:
     ```bash
     python -m pip install django-tailwind
     ```
   - Navigate to your project directory:
     ```bash
     cd projectname
     ```
   - Initialize Tailwind:
     ```bash
     python manage.py tailwind init
     ```
   - When prompted for `app_name[theme]`, type `theme`.
   - Add `'theme'` and `'django_browser_reload'` to `INSTALLED_APPS` in `settings.py`.
   - Install the browser reload package:
     ```bash
     pip install django-browser-reload
     ```

3. **Update `settings.py`**
   - Add the following lines:
     ```python
     TAILWIND_APP_NAME = 'theme'
     INTERNAL_IPS = ["127.0.0.1",]
     ```

4. **Add middleware**
   - Append the following line to the `MIDDLEWARE` list in `settings.py`:
     ```python
     "django_browser_reload.middleware.BrowserReloadMiddleware",
     ```

5. **Update `urls.py`**
   - Add the following line to the project's `urls.py` file:
     ```python
     path("reload/", include("django_browser_reload.urls")),
     ```

6. **Start Tailwind**
   - Run:
     ```bash
     python manage.py tailwind start
     


#DATABASE
---POSTGRESQL
Installations 1. Download Postgresql .exe https://www.postgresql.org/ftp/pgadmin/pgadmin4/v8.12/windows/ 2. Install Necessary, pgAdmin 3. Create the Database through pgAdmin, name it dbhrmanagement, Just check my files sa database sa settings (Right click in pgAdmin to execute commands) - General Tab then Owner is Postgres - Definition
Econding - UTF8
Tablespace -pd_default
Collation and Character - english / en_US/ - Security - Privileges - Grantee fyang - else ALL 4. create your models, modify setting.py

#DJANGO ADMIN
