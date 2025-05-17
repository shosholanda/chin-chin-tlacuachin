function showForm(button){
    CCT.Event.changeVisibility('overlay', 'flex')
}

async function deleteInsumo(button){
    if (!confirm('¿Seguro que quieres borrar este insumo?')) return;
    let url = button.getAttribute('url');
    let li = button.closest('li')
    let id_insumo = li.getAttribute('id_insumo');
    let id_producto = li.getAttribute('id_producto');
    let data = {
        'id_insumo': parseInt(id_insumo),
        'id_producto': parseInt(id_producto)
    }

    let response = await CCT.Request.fetch({url: url, data : data, type: 'POST'})
    CCT.HTML.writeOn({html: response.html, url:response.url})
}

async function displayOptions(input){
    let suggestions = document.getElementById('suggestions');
    if (input.value === "") {
        suggestions.style.display = 'none';
        return;
    }
    let list = document.getElementById('suggestions-list');
    let url = input.getAttribute('url')
    let articles = await CCT.Request.fetch({url: url + input.value})

    suggestions.style.display = 'block';
    CCT.HTML.cleanInnerHTML(list);

    for (let p of articles) {
        let attribs = { 'value': p.id }
        let selectItem = function () {
            list.innerHTML = "";
            input.value = p.nombre + " (" + p.unidad + ")";
            suggestions.style.display = 'none';
            document.getElementById('id_articulo').value = p.id
        }
        let li = CCT.HTML.createElement('li', attribs, p.nombre, 'click', selectItem);
        list.appendChild(li);
    }
}



window.onload = function () {
    let product = document.getElementById('product');
    let id_product = product.getAttribute('productID');
    let gtin = product.getAttribute('gtin');
    let url = product.getAttribute('url-status');
    let del = document.getElementById('delete');
    let upd = document.getElementById('update');

    let add_button = document.getElementById('add-art');
    add_button.addEventListener('click', function(){
        showForm(this)
    });

    let del_buts = document.getElementsByName('remove-art');
    for (let b of del_buts){
        b.addEventListener('click', function (){
            deleteInsumo(this);
        })
    }

    let art_input = document.getElementById('article')
    art_input.addEventListener('input', function(){
        displayOptions(this)
    })
    
    del.addEventListener('click', async function () {
        if (confirm('Seguro que quieres borrar este producto? No hay ninguna venta asociada todavía')){
            let response = await CCT.Request.fetch({url: del.getAttribute('url') + gtin});
            CCT.HTML.writeOn({html: response.html, url: response.url})
        }
    });

    document.getElementById('status').addEventListener('change', async function(){
        let response = await CCT.Request.fetch({url: url + gtin});
        CCT.HTML.writeOn({html: response.html, url: response.url})
    });

    upd.addEventListener('click', async function () {
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

        let response = await CCT.Request.fetch({
            url: url_update,
            type: 'POST',
            data: json
        });
        CCT.HTML.writeOn({html: response.html, url: response.url})
    });

    document.getElementById('cancel').addEventListener('click', function(){
        CCT.Event.changeVisibility('overlay')
    })
}