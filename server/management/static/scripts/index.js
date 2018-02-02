const username = "calvinfeng"
const socket = new WebSocket("ws://" + window.location.host + "/C3PO/?username=" + username);

socket.onmessage = function(e) {
    console.log(JSON.parse(e.data));
};

socket.onopen = function(e) {
    setInterval(function() {
        socket.send("Hello");
    }, 1000);
};

if (socket.readyState === WebSocket.OPEN) {
    socket.onopen();
}
