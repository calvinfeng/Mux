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