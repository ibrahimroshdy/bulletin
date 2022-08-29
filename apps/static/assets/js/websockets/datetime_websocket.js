
const user_id = JSON.parse(document.getElementById('user_id').textContent);
console.log(user_id)

const datetimeSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/datetime/'
    + user_id
    + '/'
);

datetimeSocket.onmessage = function (e) {


    const data = JSON.parse(e.data);
    var options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
    var dateObject = data.message

    //
    // document.getElementById("date").innerHTML = dateObject.toLocaleDateString("en-US", options);
    // document.getElementById("time").innerHTML = dateObject.toLocaleTimeString();

};
datetimeSocket.onclose = function (event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};
window.onbeforeunload = function () {
    datetimeSocket.onclose = function () {
    }; // disable onclose handler first
    datetimeSocket.close();
};