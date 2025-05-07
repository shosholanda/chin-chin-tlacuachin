async function popUp(answer){
    if (answer === true || answer === false){
        let url = document.getElementById('print-ticket').getAttribute('url');
        let ref = document.getElementById('sale-data').getAttribute('ref');
        let data = {'referencia': parseInt(ref), 'rfc': answer}
        let response = await CCT.Request.fetch({url: url, type: 'POST', data: data});
    }
    CCT.Event.changeVisibility('overlay', type='flex');
}

window.onload = function () {
    document.getElementById('update').addEventListener('click', async function () {
        let propina = document.getElementById('tip');
        propina = parseFloat(propina);
        let notas = document.getElementById('notes');
        let cliente = document.getElementById('client');
        let payment = CCT.HTML.getSelectedValue('payment-type');

        let data = document.getElementById('sale-data');
        let ref = data.getAttribute('ref');
        let url = data.getAttribute('url');
        let json = {
            'propina': isNaN(propina) ? 0 : propina,
            'notas': notas.value,
            'cliente': cliente.value,
            'tipo_pago': payment.value
        }
        let response = await CCT.Request.fetch({url: url + 'update-venta/' + ref, type: 'POST', data: json});
        CCT.HTML.writeOn({html: response.html, url: response.url})
    });

    document.getElementById('delete').addEventListener('click', async function () {
        if (confirm('¿Estás seguro que quieres eliminar esta venta para siempre?')){
            let data = document.getElementById('sale-data');
            let ref = data.getAttribute('ref');
            let url = data.getAttribute('url');
            let response = await CCT.Request.fetch({url: url + "delete-venta/" + ref});
            CCT.HTML.writeOn({html: response.html, url: response.url})
        }
    });

    document.getElementById('print-ticket').addEventListener('click', function(){
        popUp();
    });
    document.getElementById('cancel').addEventListener('click', function(){
        popUp();
    })

    document.getElementById('yes').addEventListener('click', function () {
        popUp(true)
    });

    document.getElementById('no').addEventListener('click', function () {
        popUp(false)
    });
}