/**
 * Cambia el id del producto dinámicamente
 */
function changeID() {
    var producto = document.getElementById('producto');
    var url = document.getElementById('url');

    // Obtenemos la ruta renderizada por jinja 
    // de
    // {{ url_for('precios.create_precio', id='') }}
    // a
    // precios/agregar-precio/
    let baseUrl = url.getAttribute('data-url-base');

    // Concatenamos el producto id
    let newUrl = baseUrl + producto.value;
    url.setAttribute("href", newUrl);
}

function statusChange(){
    let id_producto = this.id.split('-')[1]
    let id_tipo_producto = this.id.split('-')[2]

    if (!this.checked){
        // UnDelete
        fetch(`eliminar-precio/${id_producto}&${id_tipo_producto}`)
    }
    else{
        // Delete
        fetch(`deseliminar-precio/${id_producto}&${id_tipo_producto}`)
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Puros trucos.
    changeID();
    document.getElementById('producto').addEventListener('change', changeID);
    let inputs = document.getElementsByTagName('input')
    for (let i = 0; i < inputs.length; i++){
        inputs[i].addEventListener('change', statusChange);
    }

});

/* The fuck is this sort */
window.onload = function(){
    const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

    const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
        )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

    // do the work...
    document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
        const table = th.closest('table');
        Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => table.appendChild(tr) );
    })));
}