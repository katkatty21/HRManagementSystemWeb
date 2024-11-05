<!-- PROJECT LOGO -->
<br>
<div align="center">
![logoText](https://github.com/user-attachments/assets/c56ec18e-af4d-42a2-8def-772cbefbb604)
</div>

From Creating Environment Up to Github Upload

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

#DJANGO ADMIN
