const user_id2 = JSON.parse(document.getElementById('user_id').textContent);
console.log(user_id2)


const machineUptimeSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/machine_uptime/'
    + user_id2
    + '/'
);

machineUptimeSocket.onmessage = function (e) {


    const data = JSON.parse(e.data);

    uptimeDays = "<h4>" + data.message['days'] + "\t days</h4>"
    uptime = "<h4 class='text-primary'>" + data.message['hours'] + ":\t" + data.message['minutes'] + ":\t" + data.message['seconds'] + "</h4>"

    document.getElementById("uptime-days").innerHTML = uptimeDays
    document.getElementById("uptime").innerHTML = uptime
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
