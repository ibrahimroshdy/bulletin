var uptimeDays = document.getElementById("uptime-days")
var uptime = document.getElementById("uptime")
const machineUptimeUser = JSON.parse(document.getElementById('user_id').textContent);
var websocketProtocol = 'ws://'
if (location.protocol === 'https:') {
    websocketProtocol = 'wss://'
}
const machineUptimeSocket = new WebSocket(
    websocketProtocol
    + window.location.host
    + '/ws/machine_uptime/'
    + machineUptimeUser
    + '/'
);

machineUptimeSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    var d = data.message['days']
    var s = data.message['seconds']
    var m = data.message['minutes']
    var h = data.message['hours']

    uptimeDays.textContent = d + "\t days"
    uptime.textContent = ("0" + h).substr(-2) + ":" + ("0" + m).substr(-2) + ":" + ("0" + s).substr(-2);

};

machineUptimeSocket.onclose = function (event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};

window.onbeforeunload = function () {
    machineUptimeSocket.onclose = function () {
    }; // disable onclose handler first
    machineUptimeSocket.close();
};
