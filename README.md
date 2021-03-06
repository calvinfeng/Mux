# Mux
## Motivation
Mux is short for multiplexing. According wikipedia, the process of multiplexing is defined as

> A method by which multiple analog or digital signals are combined into one signal over a shared medium

In the context of Django `channels`, multiplexing means converting multiple payloads into one single source. Through
process of de-multiplexing, these payloads are then broadcast to multiple channels. This is a project for me to dive
deep into implementation of channels in Django and find a way to intercept these messages.

## File Structure
The standard file structure for Django is:
```
github_repo/
  django_project/
    manage.py
    project_name/
      settings.py
      wsgi.py
      urls.py
    app_a/
      models.py
      views.py
    app_b/
      models.py
      views.py
```

I am approaching it differently:
```
github_repo/
  django_project/
    manage.py
    settings.py
    urls.py
    wsgi.py
    app_a/
      models.py
      views.py
      ...
    app_b/
      models.py
      views.py
      ...
```

## Start new project
1. Navigate to `Mux`, create an environment, source the environment, and `pip` install the dependency.
2. Start a new project, `django-admin startproject server`.
3. Move all files from `server/server` to `server/`.
4. Rename the paths, for example `server.settings` to just `settings`.

## Create the apps
1. Create *api*, `python manage.py startapp api`
2. Create *management*, `python manage.py startapp management`
3. Add `rest_framework`, 'channels', 'management' and `api` to settings file inside `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'management'
    'rest_framework',
    'rest_framework.authtoken'
    'channels'
]
```
4. Remove `migrations/`, `admin.py`, `models.py` inside *management*.
5. Create a `templates/` folder and `urls.py` inside *management*.

## Serve static files
In the `settings.py` file, add the following:
```python
STATIC_URL = '/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "server", "management", "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "server", "management", "static")]
```

Then create a `static` folder inside management app and whatever is inside will be served at the static URL, e.g.
`localhost:8000/scripts/index.js`
