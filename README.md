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

## Channels
### Routing
```python
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'ROUTING': 'routing.channel_routing',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
            'capacity': 200,
            'expiry': 10
        }
    }
}

# Or we can use in-memory caching
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "asgiref.inmemory.ChannelLayer",
        'ROUTING': "routing.channel_routing"
    }
}
```

Notice that `routing.channel_routing` is a file we create, `routing.py`

```python
channel_routing = [
    route('websocket.receive', ws_message)
]
```

> In the example above we used the in-memory channel layer implementation as our default channel layer. This just stores
> all the channel data in a dict in memory, and so isn't actually cross-process; it only works inside runserver, as that
> runs the interface and worker servers in different threads inside the same process. When you deploy to production,
> you'll need to use a channel layer like the Redis backend asgi_redis that works cross-process.

Install `asgi_redis`
```
pip install asgi_redis
```

Install Redis on Ubuntu
```
sudo apt-get install redis-server
```

## Demultiplexer
Every demultiplexer is an abstraction over a `JsonWebsocketConsumer`.

For example, we have a `MessageDemultiplexer`:
```python
class MessageDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'message-stream': MessageBinding.consumer,
    }

    def connection_groups(self):
        return ['message-update']
```

We route it:
```python
route_class(MessageDemultiplexer, path="^/demultiplex/(?P<room_name>[a-zA-Z0-9_]+)/")
```

Whenever client hits `ws://domain:8000/demultiplex/room/`, an instance of demultiplexer is instantiated for the client,
and client will join the list of connection groups, in this case it is `message-update`. Whenever someone is broadcasting
to `message-update`, the client will also receive the updates.

When client is sending a payload of the following form:
```
{
  stream: 'message-stream',
  payload: {
    action: 'create',
    data: {
      message: 'hello world'
    }
  }
}
```
The stream name is mapping to `MessageBinding.consumer`, which means that data will be submitted to the data binding class.
Inside the data binding class, we have three methods, `create`, `update`, and `delete` and these methods are corresponding
to the `action` field inside the payload.

Now let's look at the data binding
```python
class MessageBinding(WebsocketBinding):
    model = Message
    stream = 'message-stream'
    fields = ['__all__']

    @classmethod
    def group_names(cls, instance):
        """Returns a list of groups to send outbound updates to based on the instance. Notice the instance is referring
        to the model instance that was modified. We can broadcast to different groups depending on which instance is
        modified using its id or name or whatever.

        :param Message cls: Message model class
        :param Message instance: An instance of Mesasge model class
        """
        return ['message-update']
```

Stream is referring to whenever clients are sending message to the server, the consumer of those messages will be the message binding instance. The group names tell us when models are modified, which group to broadcast the message to.
