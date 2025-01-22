
function create_type(){
    let text = document.getElementById('nuevo_tipo_de_gasto')
    if (text.value){
	let json = {'nombre': text.value}
	fetch('crear-tipo-gasto', {
            method: 'POST',
            headers: {
		'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
	}).then( response => {
	    if (response.redirected)
		window.location.href = response.url;
	    console.log("Success!", response);
	}).catch( error => console.log("Error:", error));
    } else {
	alert("Especifica un tipo de gasto.");
    }
}


function create_gasto(){
    let descripcion = document.getElementById('descripcion')
    let tipo_gasto = document.getElementById('tipo_de_gasto')
    let cantidad = document.getElementById('cantidad')
    let fecha = document.getElementById('fecha')

    if (validarCampos()){
	let json = {'tipo_de_gasto': tipo_gasto.value,
		    'cantidad': cantidad.value,
		    'descripcion': descripcion.value,
		    'fecha': fecha.value}
	fetch('create-gasto', {
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
	alert("Llena todos los campos para el gasto");
    }
}

function validarCampos(){
    let descr = document.getElementById('descripcion');
    let cant = document.getElementById('cantidad');
    let tipo = document.getElementById('tipo_de_gasto');
    return descr.value && parseInt(cant.value) && parseInt(tipo.value);
}

function deleteGasto(){
    let id_gasto = this.closest("tr").id;
    fetch(`eliminar-gasto/${id_gasto}`).then(
	response => window.location.href = response.url
    ).catch(error => console.log(error));
}

function statusChange(){
    let id_gasto = this.closest("tr").id
    fetch(`change-status/${id_gasto}`)
}

let hide = true;

window.onload = function(){

    document.getElementById('dropdown-holder').addEventListener('click', function(){
	let dpc = document.getElementById('dropdown-content').style;
	dpc.display = hide ? 'block' : 'none'
	hide = !hide;
    });

    console.log(new Date());
    document.getElementById('fecha').valueAsDate = new Date();
    document.getElementById('create-type-button').addEventListener('click', function(){
	create_type();
    });
    document.getElementById('nuevo_tipo_de_gasto').addEventListener('input', function(){
	this.value = this.value.toUpperCase();
    });
    let cgb = document.getElementById('create-gasto-button');
    cgb.addEventListener('click', function(){
	create_gasto();
    });
    cgb.disabled = true;
    
    document.getElementById('cantidad').addEventListener('input', function(){
	cgb.disabled = validarCampos() ? false : true;
	
    });
    document.getElementById('descripcion').addEventListener('input', function(){
	cgb.disabled = validarCampos() ? false : true;
    });

    let statuses = document.getElementsByName('status');
    let borrars = document.getElementsByName('borrar');
    
    for (let i = 0; i < statuses.length; i++){
	borrars[i].addEventListener('click', deleteGasto);
	statuses[i].addEventListener('change', statusChange);
    }
}

