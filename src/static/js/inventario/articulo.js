async function deleteArticulo() {
    let url = document.getElementById('delete');
    url = url.getAttribute('url');
    let response = await CCT.Request.fetch({url: url});
    CCT.HTML.writeOn({html: response.html, url: response.url})
}

async function updateArticulo() {
    let tipo_articulo = CCT.HTML.getSelectedValue('article-type').value
    let unidad = document.getElementById('unit').value;
    let costo = document.getElementById('cost-per-unit').value;

    let cantidad_actual = document.getElementById('present-quantity').value;
    cantidad_actual = math.evaluate(cantidad_actual);
    let min = document.getElementById('min').value;
    let max = document.getElementById('max').value;
    max = isNaN(parseFloat(max)) ? 0 : max
    let url = document.getElementById('update').getAttribute('url');
    console.log(tipo_articulo, unidad, costo, cantidad_actual, min, max, url)

    if (CCT.Text.validateString(unidad, url) && CCT.Text.validateInt(tipo_articulo) 
        && CCT.Text.validateDouble(costo, cantidad_actual, min, max)){
        let json = {
            'cantidad_actual': parseFloat(cantidad_actual),
            'tipo_articulo': parseInt(tipo_articulo),
            'unidad': unidad,
            'costo': parseFloat(costo),
            'minimo': parseFloat(min),
            'maximo': parseFloat(max)
        }

        let response = await CCT.Request.fetch({url: url, type:'POST', data: json})
        CCT.HTML.writeOn({html: response.html, url: response.url})
    }
}

window.onload = function () {

    document.getElementById('delete').addEventListener('click', function () {
        if (confirm('Seguro que quieres eliminar este articulo?'))
            deleteArticulo();
    })

    document.getElementById('update').addEventListener('click', function () {
        updateArticulo();
    });
}