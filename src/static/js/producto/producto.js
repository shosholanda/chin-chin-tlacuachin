
window.onload = function () {
    let product = document.getElementById('product');
    let id_product = product.getAttribute('productID');
    let gtin = product.getAttribute('gtin');
    let url = product.getAttribute('url-status');
    let del = document.getElementById('delete');
    let upd = document.getElementById('update');
    
    del.addEventListener('click', function () {
        if (confirm('Seguro que quieres borrar este producto? No hay ninguna venta asociada todavía'))
            CCT.Request.fetch({url: del.getAttribute('url') + gtin});
    });

    document.getElementById('status').addEventListener('change', async function(){
        await CCT.Request.fetch({url: url + gtin});
    });

    upd.addEventListener('click', function () {
        let precio = document.getElementById('price');
        if (!CCT.Text.validateDouble(precio.value)){
            alert('Precio nuevo no aceptado');
            return;
        }
        let url_update = this.getAttribute('url');
        let json = {
            // 'id_producto': parseInt(id_product),
            'gtin': gtin,
            // 'nombre': gtin, // May these two change
            'precio': parseFloat(precio.value)
        }

        CCT.Request.fetch({
            url: url_update,
            type: 'POST',
            data: json
        });
    })
}