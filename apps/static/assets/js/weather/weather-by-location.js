const navigatorOptions = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};

function success(pos) {
    const crd = pos.coords;

    getWeatherByLocAjax(crd, function (response) {
        console.log(response)
        document.getElementById("temp").innerHTML = response.main.temp.toFixed(0) + '&deg;';
        document.getElementById("location-name").textContent = response.name;
        document.getElementById("condition-icon").src = "https://openweathermap.org/img/wn/" + response.weather[0].icon + "@4x.png";
        document.getElementById("wind").textContent = response.wind.speed + "kph";
        document.getElementById("condition-text").innerHTML = response.weather[0].main;


    })
}

function error(err) {
    console.warn(`ERROR(${err.code}): ${err.message}`);
}

navigator.geolocation.getCurrentPosition(success, error, navigatorOptions);

//TODO: api key to env varible
function getWeatherByLocAjax(crd, callback) {
    $.ajax({
        url: "https://api.openweathermap.org/data/2.5/weather?" + "" +
            "lat=" + crd.latitude +
            "&lon=" + crd.longitude +
            "&units=metric" +
            "&appid=daccc7287e75d7ad0c14b58539755543",
        type: "GET",
        dataType: "json",
        success: (data) => {
            callback(data);
        },
        error: (error) => {
            console.log(error);
        }

    });

};

// function ajaxCallback() {
// };