function deleteGasto() {
    let url = document.getElementById('delete');
    url = url.getAttribute('url');
    CCT.Request.fetch({url: url});
}

function updateGasto() {
    let tipo_gasto = CCT.HTML.getSelectedValue('type').value
    let cantidad = document.getElementById('quantity').value;
    let descripcion = document.getElementById('description').value;

    let fecha = document.getElementById('date').value;
    let status = document.getElementById('status').value;
    let url = document.getElementById('update-data').getAttribute('url')

    if (CCT.Text.validateString(descripcion, fecha) && CCT.Text.validateInt(tipo_gasto) 
        && CCT.Text.validateDouble(cantidad)){
        let json = {
            'tipo_gasto': parseInt(tipo_gasto),
            'cantidad': parseFloat(cantidad),
            'descripcion': descripcion,
            'fecha': fecha,
            'status': status
        }
        CCT.Request.fetch({url: url, type:'POST', data: json})
    }
}

window.onload = function () {
    document.getElementById('delete').addEventListener('click', function () {
        if (confirm('Seguro que quieres eliminar este gasto?'))
            deleteGasto();
    })

    document.getElementById('update-data').addEventListener('click', function () {
        updateGasto();
    });
}