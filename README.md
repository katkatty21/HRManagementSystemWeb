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

The **HR Management System** is a comprehensive platform designed to streamline and optimize the core functions of Human Resources. Built to simplify processes like employee data management, attendance tracking, payroll processing, performance evaluations, and recruitment, this system serves as an all-in-one solution for HR departments of any size. By centralizing data and automating repetitive tasks, it reduces administrative workload and helps HR teams focus on strategic activities, such as talent development and employee engagement.


### Key Features
- **Employee Profiles**: Centralized database for managing employee records and personal information.
- **Attendance Management**: Efficiently track attendance, leaves, and absences with real-time counts for absentees, leaves, and those present, while providing comprehensive records, with overtime and  regular hours record to ensure transparency and accountability.
- **Payroll Management**: Automated calculations, deductions, and payments with secure storage and accessibility
- **Performance Management**: Tools for peer feedback, self-assessment, supervisor feedback, and sanction reporting
- **Recruitment Tools**: Simplifies the hiring process with applicant tracking, resume management, and scheduling capabilities.
- **Analytics Dashboard**: Real-time insights into HR data to support decision-making and compliance.




## Built With  

- **Backend**: Django (Python) - A high-level web framework for efficient and scalable backend development.  
- **Database**: PostgreSQL - A powerful and reliable database system for managing structured data.  
- **Frontend**: Tailwind CSS - A utility-first CSS framework for designing responsive and customizable user interfaces.  


## Getting Started

### Prerequisites
Ensure you have the following:
- Python 3.x
- Django installed in a virtual environment
- PostgreSQL with `pgAdmin`
- Basic understanding of Django ORM and SQL

### Installation

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

1. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

3. **Access the Application**
   Visit `http://127.0.0.1:8000/` in your browser.

4. **Explore Features**
   - Leverage the Django admin panel for CRUD operations.
   - Use the Tailwind-enhanced interface for a smooth user experience.



## Contact


  
- [Sophie Anneka Seismundo](sophieanneka.seismundo@cit.edu): sophieanneka.seismundo@cit.edu
- [Katrina Amores](https://github.com/katkatty21): katrina.amores@cit.edu
- [Rey Christian Bacolod](https://github.com/rychfghg): reychristian.bacolod@cit.edu



## Additional Resources

- [Functional Requirements Document](https://docs.google.com/document/d/1wRUX7TfamZ61ei4otYVEJMC07NCnUOh7NaZMVRlH61s/edit?tab=t.0)
- [Gantt Chart:](https://docs.google.com/spreadsheets/d/100kTUpP4Sychp47k7l7S2iiFd9uNb3wG9xwUYE7GOIQ/edit?gid=0#gid=0)
- [Entity Relationship Diagram](https://www.figma.com/board/mmlZjU6REvV2qqFbcbgqqv/Physical-ERD?node-id=2-485&node-type=table&t=r4o1MAyiJLQqJKMD-0)
- [UI/UX](https://www.figma.com/design/KOYZs82m0yT8wV7tcVyIjb/HR-Management-System-UI-UX?node-id=0-1&node-type=canvas&t=gFdfWWqKWUHT7CSz-0)



## Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Special thanks to the open-source community.





