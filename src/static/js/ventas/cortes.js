async function sendData(url){
    let s_date = document.getElementById('start-date').value;
    let f_date = document.getElementById('end-date').value;
    let filter = CCT.HTML.getSelectedValue('filter').value;
    let period = document.getElementById('get-data').getAttribute('period')

    if (!CCT.Text.validateString(s_date)) {
        alert("Selecciona un día para consultar las ventas ese día");
        return
    }
    

    let data = {
        'start_date': s_date,
        'end_date': f_date,
        'filter': parseInt(filter),
        'period': period
    }
    let response = await CCT.Request.fetch({url: url, data: data, type: 'POST'})
    let container = document.getElementsByClassName('container')[0];
    CCT.HTML.writeOn({html: response.html, element: container})

}


window.onload = function(){
    let query_button = document.getElementById('get-data');

    query_button.addEventListener('click', function(){
        let url = this.getAttribute('url')
        sendData(url)
    })
}