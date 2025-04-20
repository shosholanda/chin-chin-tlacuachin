function popUp(answer){
    if (answer === true){
        let data = document.getElementById('sale-data');
        let ref = data.getAttribute('ref');
        let url = data.getAttribute('url');
        CCT.Request.fetch({url: url + "delete-venta/" + ref, redirect: 'manual'});
    }
    CCT.Event.changeVisibility('overlay', type='flex');
}

window.onload = function () {
    document.getElementById('update').addEventListener('click', function () {
        let propina = document.getElementById('tip');
        let notas = document.getElementById('notes');
        let cliente = document.getElementById('client');

        let data = document.getElementById('sale-data');
        let ref = data.getAttribute('ref');
        let url = data.getAttribute('url');
        let json = {
            'propina': parseInt(propina.value),
            'notas': notas.value,
            'cliente': cliente.value
        }
        CCT.Request.fetch({url: url + 'update-venta/' + ref, type: 'POST', data: json, redirect: 'manual'});
    });

    document.getElementById('delete').addEventListener('click', function () {
        popUp();
    })

    document.getElementById('yes').addEventListener('click', function () {
        popUp(true)
    });

    document.getElementById('no').addEventListener('click', function () {
        popUp()
    });
}