// tbl = document.getElementById("twt-trends-table");
// tbl.style.width = '100px';
// tbl.style.border = '1px solid black';
// getTwitterTrendsbyAjax(function (response) {
//     for (var [country, trends] of Object.entries(response)) {
//         const tr = tbl.insertRow()
//         tr.appendChild(document.createTextNode(country))
//         console.log(country, trends)
//
//         for (var [key, value] of Object.entries(trends.trends)) {
//             console.log(key, value)
//             const td = tr.insertCell()
//             td.appendChild(document.createTextNode(value.name))
//         }
//     }
//
//
// })
//
//
// function getTwitterTrendsbyAjax(callback) {
//     $.ajax({
//         url: window.location.href +
//             'twt_get_trends',
//         type: "GET",
//         dataType: "json",
//         success: (data) => {
//             callback(data);
//         },
//         error: (error) => {
//             console.log(error);
//         }
//     });
// }