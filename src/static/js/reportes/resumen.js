var lineChart;

async function getData(start, end, url){
    let data = {
        'start-date': start,
        'end-date': end
    }

    let response = await CCT.Request.fetch({url: url, data: data});

    let totals = document.getElementsByClassName('container')[0];
    CCT.HTML.writeOn({html: response.container, element: totals})
    drawGraph(response.x_data, response.y_data)
}

function drawGraph(x_data, y_data){
    var ctx = document.getElementById('the-canvas').getContext("2d");
    if (lineChart){
        lineChart.clear();
        lineChart.destroy();
    }
    
    lineChart = new Chart(ctx, {
        type: "line",
        data: {
            // x-axis
            labels: x_data,
            datasets: [
                {   //y-axis
                    label: "Ganancia bruta ",
                    data: y_data.ganancia_bruta, 
                    borderColor: "rgb(75, 192, 192)"
                }, {
                    label: "Costo productos",
                    data: y_data.costos_productos,
                    borderColor: 'orange'
                }, {
                    label: "Utilidad bruta",
                    data: y_data.utilidad_bruta,
                    borderColor: 'blue'
                }, {
                    label: "Costos Fijos",
                    data: y_data.costos_fijos,
                    borderColor: 'red'
                }, {
                    label: "Utilidad neta",
                    data: y_data.utilidad_neta,
                    borderColor: 'green'
                }, {
                    label: "Promedio",
                    data: y_data.promedio,
                    borderColor: 'black',
                    fill: true
                }
            ]
        }, 
        options: {
            responsive: true

        }
    });
}

window.onload = function(){

    let ini = document.getElementById("start-date");
    let fin = document.getElementById("end-date");
    let button = document.getElementById("evaluate");


    button.addEventListener('click', function(){
        getData(ini.value, fin.value, this.getAttribute('url'));
    })
}