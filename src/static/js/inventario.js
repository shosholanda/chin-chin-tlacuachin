// import { Macros } from "./macros.js"; WEEEEY POR QUE TIENE QUE SER TAN DIFICIL ????????

function toTitleCase(str) {
    return str.replace(
	/\w\S*/g,
	text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
    );
}

function create_articulo(){
    let nombre = document.getElementById('nombre')
    let cantidad_actual = document.getElementById('cantidad_actual')
    let unidad = document.getElementById('unidad')
    let costo_por_unidad = document.getElementById('costo_por_unidad')
    let min = document.getElementById('minimo');
    let max = document.getElementById('maximo');
    
    if (validarCampos()){
	let json = {'nombre': nombre.value,
		    'cantidad_actual': cantidad_actual.value,
		    'unidad': unidad.value,
		    'costo_por_unidad': costo_por_unidad.value,
		    'minimo': min.value,
		    'maximo': max.value}
	fetch('create-articulo', {
            method: 'POST',
            headers: {
		'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
	}).then( response => {
	    if (response.redirected)
		window.location.href = response.url
	}).catch( error => console.log("Error:", error));
    } else {
	alert("Llena todos los campos para el articulo");
    }
}

function validarCampos(){
    let nom = document.getElementById('nombre')
    let can = document.getElementById('cantidad_actual')
    let uni = document.getElementById('unidad')
    let cos = document.getElementById('costo_por_unidad')
    let min = document.getElementById('minimo');
    let max = document.getElementById('maximo');
    return nom.value && parseInt(can.value) && parseInt(cos.value) &&
	uni.value && parseInt(min.value);
}

function deleteArticulo(){
    let id_articulo = this.closest("tr").id;
    fetch(`eliminar-articulo/${id_articulo}`).then(
	response => window.location.href = response.url
    ).catch(error => console.log(error));
}

function statusChange(){
    let id_articulo = this.closest("tr").id
    fetch(`change-status/${id_articulo}`)
}

let hide = true;

window.onload = function(){

    document.getElementById('dropdown-holder').addEventListener('click', function(){
	let dpc = document.getElementById('dropdown-content').style;
	dpc.display = hide ? 'block' : 'none'
	hide = !hide;
    });

    let cab = document.getElementById('create-article-button');
    cab.addEventListener('click', function(){
	create_articulo();
    });
    cab.disabled = true;
    
    document.getElementById('cantidad_actual').addEventListener('input', function(){
	cab.disabled = validarCampos() ? false : true;	
    });
    document.getElementById('nombre').addEventListener('input', function(){
	this.value = toTitleCase(this.value);
	fetch(`get-articulo/${this.value}`).then( response =>
	    response.json().then( response => {
		if (response.id){
		    cab.disabled = true;
		    alert("Este producto ya existe, intenta otro nombre");
		}
	    })
	).catch(e => console.log(e))
	cab.disabled = validarCampos() ? false : true;
    });
    document.getElementById('unidad').addEventListener('input', function(){
	cab.disabled = validarCampos() ? false : true;
    });
    document.getElementById('costo_por_unidad').addEventListener('input', function(){
	cab.disabled = validarCampos() ? false : true;
    });
    document.getElementById('minimo').addEventListener('input', function(){
	cab.disabled = validarCampos() ? false : true;
    });


    let statuses = document.getElementsByName('status');
    
    for (let i = 0; i < statuses.length; i++){
	statuses[i].addEventListener('change', statusChange);
    }
}

