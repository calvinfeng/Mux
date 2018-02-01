const socket = new WebSocket("ws://" + window.location.host);
const id = Math.random();

socket.onmessage = function(e) {
    console.log(JSON.parse(e.data));
};

socket.onopen = function(e) {
    setInterval(function() {
        socket.send(JSON.stringify({
            user_id: id,
            message: "Hello"
        }));
    }, 1000);
};

if (socket.readyState === WebSocket.OPEN) {
    socket.onopen();
}
