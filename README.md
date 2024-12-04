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
    <li><a href="#contact">Contact</a></li>
     <li><a href="#additional-resources">Additional Resources</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

The HR Management System is a comprehensive platform designed to streamline and optimize the core functions of Human Resources. Built to simplify processes like employee data management, attendance tracking, payroll processing, performance evaluations, and recruitment, this system serves as an all-in-one solution for HR departments of any size. By centralizing data and automating repetitive tasks, it reduces administrative workload and helps HR teams focus on strategic activities, such as talent development and employee engagement.

Key features include:

- Employee Profiles: Centralized database for managing employee records and personal information.
- Attendance Management: Efficiently track attendance, leaves, and absences with real-time counts for absentees, leaves, and those present, while providing comprehensive records, with overtime and  regular hours record to ensure transparency and accountability.
- Payroll Management: Automated calculations, deductions, and payments with secure storage and accessibility
- Performance Management: Tools for peer feedback, self-assessment, supervisor feedback, and sanction reporting
- Recruitment: Simplifies the hiring process with applicant tracking, resume management, and scheduling capabilities.
- Reporting and Analytics: Real-time insights into HR data to support decision-making and compliance.



## Built With


- **Python Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **PostgreSQL**: A powerful, open-source object-relational database system.


- **CSS Framework: Tailwind CSS**: A utility-first CSS framework for creating custom designs directly in your markup.



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



## Prerequisites

- Python 3.x installed and configured.
- Django installed in a virtual environment.
- PostgreSQL installed with `pgAdmin`.
- Basic understanding of SQL and Django ORM.

## Installation



**Tailwind CSS Framework Setup** 


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


**PostgreSQL Installation** 


1. **Download PostgreSQL Installer**
   - Download the PostgreSQL `.exe` from the following link:
     [PostgreSQL Download](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v8.12/windows/)

2. **Install Required Components**
   - During installation, ensure that `pgAdmin` is selected as a component.

3. **Create the Database**
   - Open `pgAdmin`.
   - Create a new database:
     - Right-click on `Databases` > `Create` > `Database`.
     - Name the database `dbhrmanagement`.
     - In the **General Tab**, set the **Owner** to `postgres`.
   - Check the database files in `pgAdmin` for additional settings or configurations.
   - Use the **Definition Tab** for further configuration if necessary.

4. **Execute Commands in pgAdmin**
   - To run SQL commands, right-click on the database and select `Query Tool`.


## Usage

- Start the PostgreSQL service and ensure it is running.
- Use `pgAdmin` for database management and to execute SQL queries if needed.
- Run `python manage.py makemigrations` and `python manage.py migrate` in your Django project to apply model changes to the database.
- Implement database interactions using Django ORM and design a user-friendly interface for performing CRUD operations. Utilize Tailwind CSS to ensure responsive and visually appealing design.


## Contact

- Sophie Seismundo; sophie.seismundo@cit.edu
- Katrina Amores: katrina.amores@cit.edu
- Rey Christian Bacolod: reychristian.bacolod@cit.edu


## Acknowledgments

- PostgreSQL documentation: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- Django documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Special thanks to the contributors of open-source tools used in this project.


## Additional Resources 

- Functional Requirements Document: 
- Gantt Chart:
- Entity Relationship Diagram (ERD): 






