async function create_articulo() {
    let nombre = document.getElementById('name')
    let tipo_articulo = document.getElementById('article-type')
    let cantidad_actual = document.getElementById('present-quantity')
    let unidad = document.getElementById('unit')
    let costo_por_unidad = document.getElementById('cost-per-unit')
    let min = document.getElementById('min');
    let max = document.getElementById('max');
    let url = document.getElementById('create-article-button').getAttribute('url');

    if (validarCamposArticulo()) {
        let json = {
            'nombre': nombre.value,
            'tipo_articulo': tipo_articulo.value,
            'cantidad_actual': cantidad_actual.value,
            'unidad': unidad.value,
            'costo_por_unidad': costo_por_unidad.value,
            'minimo': min.value,
            'maximo': max.value
        }
        let response = await CCT.Request.fetch({url: url, data: json, type: 'POST'});
        CCT.HTML.writeOn({html: response.html, url: response.url})

    } else {
        alert("Llena todos los campos para el articulo");
    }
}

async function create_tipo() {

    let nuevo_tipo_articulo = document.getElementById('new-article-type').value;
    let url = document.getElementById('create-type-button').getAttribute('url');

    if (CCT.Text.validateString(nuevo_tipo_articulo)) {
        json = { 'tipo_articulo': nuevo_tipo_articulo };
        let response = await CCT.Request.fetch({url: url, type: 'POST', data: json});
        CCT.HTML.writeOn({html: response.html, url: response.url})
    }
}

function validarCamposArticulo() {
    let nom = document.getElementById('name').value;
    let tip = CCT.HTML.getSelectedValue('article-type').value;
    let can = document.getElementById('present-quantity').value;
    let uni = document.getElementById('unit').value;
    let cos = document.getElementById('cost-per-unit').value;
    let min = document.getElementById('min').value;
    let max = document.getElementById('max').value;

    return CCT.Text.validateString(nom, uni) && CCT.Text.validateInt(tip, can, min)
        && CCT.Text.validateDouble(cos);
}

function statusChange() {
    let id_articulo = this.closest("tr").id
    fetch(`change-status/${id_articulo}`)
}


window.onload = function () {

    let nuevo_articulo_button = document.getElementById('dropdown-holder');
    let menu_crear_articulo = document.getElementById('dropdown-content');
    let menu_crear_tipo = document.getElementById('category-form');
    let nuevo_tipo_button = document.getElementById('create-new-type');
    let nuevo_tipo_input = document.getElementById('new-article-type');
    let crear_tipo_button = document.getElementById('create-type-button');
    let crear_articulo_button = document.getElementById('create-article-button');

    nuevo_articulo_button.addEventListener('click', function () {
        CCT.Event.changeVisibility(menu_crear_articulo);
    });
    
    crear_articulo_button.addEventListener('click', function () {
        create_articulo();
    });

    nuevo_tipo_button.addEventListener('click', function () {
        CCT.Event.changeVisibility(menu_crear_tipo, 'flex');
    });

    nuevo_tipo_input.addEventListener('input', function(){
        this.value = this.value.toUpperCase();
    });

    crear_tipo_button.addEventListener('click', function(){
        create_tipo();
    });
    
    CCT.HTML.get('name').addEventListener('input', function(){
        this.value = CCT.Text.toTitleCase(this.value);
    });

    

    let statuses = document.getElementsByName('status');

    for (let i = 0; i < statuses.length; i++) {
        statuses[i].addEventListener('change', statusChange);
    }
}

