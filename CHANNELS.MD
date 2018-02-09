# Channels
## Layer Setup
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

## Concept
> An ordered, first-in first-out queue with message expiry and at-most-once delivery to only one listener at a time.

Write a function to consume a channel
```python
def example_consumer(message):
    pass
```

Route it
```python
channel_routing = [
  route('channel-name', example_consumer, path="^/example$"),
]
```

*Question: How are workers spawn to handle the execution of the `example_consumer` block of code?* What we know is that
the workers are listening on all relevant channels and run consumer code whenever a message is ready. This is equivalent
to spawning a goroutine to do something like:
```go
exampleChan := make(chan int)

go func() {
  for val := range exampleChan {
    // Listening
    consumerCallback(val)
  }
}()
```

Every consumer is given a response channel, called `reply_channel`, e.g.
```python
def example_consumer(message):
    message.reply_channel.send("Thanks for connecting to our websocket.")
```

This is equivalent to
```go
type Message struct {
  Reply chan int
  Data int
}

exampleChan := make(chan int)
reply := make(chan int)
go func() {
  input := range exampleChan {
    consumerCallback(Message{
        Reply: reply,
        Data: input
    })
  }
}
```

## Groups
Group is like a collection of reply_channels. Since each channel can only communicate with one connection (i.e. one client),
`group` abstracts away the need to broadcast message by iterating through all the reply channels.
```python
Group('sas-team').send({"text": "Meeting time, get your ass to the meeting room."})
```

Inside the consumer callback, simply add the client to a group to receive broadcasts.
```python
def example_consumer(message):
    Group('sas-team').add(message.reply_channel)
```

Group can also automatically expires group members. I don't exactly know the expiry policy at the moment. If a group does
not receive any message for a long time, the reply channels get expired automatically and become garbage collected. We can
also remove a member from the group manually.
```python
def on_disconnect_callback(message):
  Group('sas-team').discard(message.reply_channel)
```

## Class-based Consumer
The `BaseCosnumer` class allows you specify channel mapping to callbacks. The default channels are `websocket.connect`,
`websocket.receive`, and `websocket.disconnect`. We can perform a channel mapping using `BaseConsumer`:
```python
class ExampleConsumer(BaseConsumer):
    method_mapping = {
        "websocket.receive": "handle_receive"
    }

    def handle_receive(self, message, **kwargs):
        pass
```

### Websocket & JSON Consumer
This further abstracts the code above into a class that has `receive`, `disconnect`, and `connect` methods.
```python
class ExampleWebsocketConsumer(WebsocketConsumer):
    def connection_groups(self, **kwargs):
        return ['sas']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        self.send(text="Welcome to SAS channel", bytes=bytes)

    def disconnect(self, message, **kwargs):
        pass

If you want text to be serialized into JSON by default, then use `JsonWebsocketConsumer`.
```python
class ExampleJSONWebsocketConsumer(JsonWebsocketConsumer):
    def connection_groups(self, **kwargs):
        return ['sas']

    def connect(self, message, **kwargs):
        pass

    def receive(self, content, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        pass
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
