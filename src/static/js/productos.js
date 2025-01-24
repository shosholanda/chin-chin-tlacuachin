function toTitleCase(str) {
    return str.replace(
	/\w\S*/g,
	text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
    );
}

function generateGtin(){
    /* Selecciona las 2 primeras letras de cada palabra */
    function generateCode(s, i=2){
	s = s.toUpperCase();
	if (s.length < 2) return "";
	if (s.length === 2) return s;
	return s.split(' ').map(w => {
	    if (w.length <= 2)
		return ""
	    return w.substring(0,i);
	}).join("");
    }
    
    let code = ""
    let nombre = document.getElementById('nombre')
    let categoria = document.getElementById('categoria')
    let tipo_producto = document.getElementById('tipo_de_producto')
    let precio = document.getElementById('precio')
    if (nombre)
	nombre = generateCode(nombre.value, 4)
    if (categoria.options.length)
	categoria = generateCode(categoria.options[categoria.selectedIndex].text)
    else
	categoria = ""
    if (tipo_producto.options.length)
	tipo_producto = generateCode(tipo_producto.options[tipo_producto.selectedIndex].text)
    else tipo_producto = ""
    if (precio)
	precio = precio.value

    code = nombre + categoria + tipo_producto + precio;

    fetch('get-gtin/'+ code).then(
	response => response.json().then(
	response => {
	    let gtin = response['gtin']
	    if (gtin){
		alert(`Ya existe un producto con este código: ${gtin}\n
Utiliza otros datos, o cambia manualmente el gtin`);
		document.getElementById('create-product-button').disabled = true;
	    }
	    else if (nombre && categoria && tipo_producto && precio){
		document.getElementById('create-product-button').disabled = false;
	    }
	    
	    
	})
    ).catch( error => console.log("Error:", error));
    return code;
}

function create_category(){
    let text = document.getElementById('nueva_categoria')
    if (text.value){
	let json = {'nombre': text.value}
	fetch('crear-categoria', {
            method: 'POST',
            headers: {
		'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
	}).then( response => response.text().then(
	    response => {
		// console.log("Success!", response);
		location.reload();
	    })
	       ).catch( error => console.log("Error:", error));
    } else {
	alert("Especifica una categoria");
    }
}

function create_type(){
    let text = document.getElementById('nuevo_tipo_de_producto')
    if (text.value){
	let json = {'nombre': text.value}
	fetch('crear-tipo-producto', {
            method: 'POST',
            headers: {
		'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
	}).then( response => response.text().then(
	    response => {
		console.log("Success!");
		location.reload();
	    })
	       ).catch( error => console.log("Error:", error));
    } else {
	alert("Especifica un tipo de producto.");
    }
}


function create_product(){
    let nombre = document.getElementById('nombre')
    let categoria = document.getElementById('categoria')
    let tipo_producto = document.getElementById('tipo_de_producto')
    let precio = document.getElementById('precio')
    let gtin = document.getElementById('gtin')

    if (nombre.value && categoria.value && tipo_producto.value && precio.value && gtin.value){
	let json = {'nombre': nombre.value,
		    'categoria': categoria.value,
		    'tipo_producto': tipo_producto.value,
		    'precio': precio.value,
		    'gtin': gtin.value }
	console.log(json)
	fetch('create-producto', {
            method: 'POST',
            headers: {
		'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
	}).then( response => response.text().then(
	    response => {
		console.log("Success!");
		location.reload();
	    })
	       ).catch( error => console.log("Error:", error));
    } else {
	alert("Llena todos los campos para el producto");
    }
}

function deleteProducto(){
    let gtin = this.closest("tr").id;
    fetch(`eliminar-producto/${gtin}`)
    location.reload();
}

function statusChange(){
    let gtin = this.closest("tr").id
    fetch(`change-status/${gtin}`)
}

let hide = true;

window.onload = function(){

    document.getElementById('dropdown-holder').addEventListener('click', function(){
	let dpc = document.getElementById('dropdown-content').style;
	dpc.display = hide ? 'block' : 'none'
	hide = !hide;
    });

    let create_category_button = document.getElementById('create-category-button');
    let create_type_button = document.getElementById('create-type-button');
    let create_product_button = document.getElementById('create-product-button');
    create_product_button.disabled = true;
    let gtin_input = document.getElementById('gtin');
    gtin_input.value = generateGtin();
    let nombre_input = document.getElementById('nombre');
    let categoria_input = document.getElementById('categoria');
    let tipo_producto_input = document.getElementById('tipo_de_producto');
    let precio_input = document.getElementById('precio');
    let statuses = document.getElementsByName('status');
    let borrars = document.getElementsByName('borrar');
    for (let i = 0; i < statuses.length; i++){
	borrars[i].addEventListener('click', deleteProducto);
	statuses[i].addEventListener('change', statusChange);
    }




    create_category_button.addEventListener('click', function(){
	create_category();
    });

    create_type_button.addEventListener('click', function(){
	create_type();
    });

    create_product_button.addEventListener('click', function(){
	create_product();
    });

    nombre_input.addEventListener('input', function(){
	gtin_input.value = generateGtin();
	this.value = toTitleCase(this.value)
    });

    precio_input.addEventListener('input', function(){
	gtin_input.value = generateGtin();
    });

    categoria_input.addEventListener('change', function(){
	gtin_input.value = generateGtin();
    });

    tipo_producto_input.addEventListener('change', function(){
	gtin_input.value = generateGtin();
    });

    gtin_input.addEventListener('input', function(){
	gtin_input.value = generateGtin();
    });
    
}

