/**
 * Generamos dinámicamente el carro, pero no se guarda nada hasta q se confirme
 */

var carro = [];

/* Crea un pedido */
function nuevoItem(gtin, cantidad) {
    let cart = document.getElementById('cart');
    fetch('get-gtin/'+ gtin).then(
	response => response.json().then(
	    response => {
		response.gtin = gtin;
		response.cantidad = cantidad;
		carro.push(response);
		let id = response['id'];
		let nombre = response['nombre'];
		let precio = response['precio'];
		let subtotal = precio*cantidad;
		let itemString =  `<div class="item">
    <div class="item" id="${id}">
      <div>
	<div>
	 ${gtin}
	</div>
	<div>
	  ${nombre}
	</div>
      </div>
    </div>
    <div>
      <div class="campo">
        <label for="cantidad">Cantidad</label>
        <input type="number" id="cantidad" name="cantidad" required="true" autocomplete="off" min="1" value="${cantidad}">
      </div>
        <div>
          Precio:$ ${precio}
        </div>
    </div>
    <div>
      <h5>Subtotal</h5>
      <p>$ ${subtotal}</p>
    </div>
  </div>`
		cart.insertAdjacentHTML('beforeend', itemString);
		updateTotal();
		resetInput();
	    }
	)
    ).catch( error => console.log("Error:", error));
    
    
    
}

function resetInput(){
    document.getElementById('codigo_gtin').value = ""
    document.getElementById('cantidad').value = "";
}

function updateTotal(){
    let total = document.getElementById('total')
    let x = 0;
    for (let item of carro){
	x += item.precio*item.cantidad;
    }
    total.value = x;
}

function agregarProducto(){
    let gtin = document.getElementById('codigo_gtin');
    let cant = document.getElementById('cantidad');

    if (!(gtin.value && cant.value)){
	// document.getElementById('agregar').disabled = true;
	return;
    }

    nuevoItem(gtin.value, parseInt(cantidad.value));
}


function buscaGtin(){
    pseudogtin = this.value.toUpperCase();
    this.value = pseudogtin;
    let suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = "";
    
    if (!(pseudogtin)) return;
    fetch('get-gtins/'+ pseudogtin).then(
	response => response.json().then(
	    response => {
		let gtins = response['gtins']
		for (const [key, value] of Object.entries(gtins)){
		    agregaLista(suggestions, key, value);
		}
	    }
	)
    ).catch( error => console.log("Error:", error));
    
}

function agregaLista(uList, value, text){
    let li = document.createElement('li');
    li.setAttribute('value', value);
    li.addEventListener('click', function () {
	let suggestions = document.getElementById('suggestions');
	let gtin = document.getElementById('codigo_gtin');
	suggestions.innerHTML = "";
	gtin.value = value
    });
    li.textContent = text
    uList.appendChild(li);
    
}

/**
 * Envia las compras agregadas anteriormente al cart.
 * Crea un JSON con la información colectada por el cart
 */
function sendCart(){
    //Convertir a JSON
    let cartData = [];


    for (let item of carro){
	let p = item.id;
	let c = item.cantidad;
	
        let data = {
	    id_producto: p,
            cantidad: c
        };
	cartData.push(data);
    }

    let cliente = document.getElementById('cliente');
    let notas = document.getElementById('notas');
    let propina = document.getElementById('propina');
    let total = document.getElementById('total');

    let shop = {
        cart: cartData,
        total: total.value,
	propina: propina.value,
	notas: notas.value,
	cliente: cliente.value
    }


    //Enviar JSON
    fetch('create-venta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(shop)
    })
	.then(response => {
            return response.text().then(text => {
		// return JSON.parse(text); // Todos coludos o todos rabones
		return text;
            });
	})
	.then(html => {
            // Por JSON
            // if (data.redirect) {
            //     // window.location.href = data.redirect;
            // } else {
            //     console.log('Success:', data);
            // }
            document.open();
            document.write(html);
            document.close();

	})
	.catch((error) => {
            console.log('Error:', error);
	});
}

// Main
window.onload = function (){
    let agregar_button = document.getElementById('agregar');
    let codigo_input = document.getElementById('codigo_gtin');
    let cant = document.getElementById('cantidad');
    let comprar = document.getElementById('comprar');

    agregar_button.addEventListener('click', agregarProducto);
    codigo_input.addEventListener('input', buscaGtin);
    comprar.addEventListener('click', sendCart);
}

window.addEventListener('beforeunload', function (e) {
    var confirmationMessage = 'Are you sure you want to leave this page?';
    e.returnValue = confirmationMessage;  // Gecko, WebKit, Chrome <34
    return confirmationMessage;           // Gecko, WebKit, Chrome >=34
});

