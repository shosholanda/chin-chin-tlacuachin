/**
 * Generamos dinámicamente el carro, pero no se guarda nada hasta q se confirme
 */

var counter = 0;

/* Crea un pedido */
async function createBox(producto, tipo, cantidad) {
    let item = document.createElement('div');
    item.className = 'item';

    //Crear más bonita la caja
    var div, label, id;

    /* Producto */
    div = document.createElement('div');
    div.setAttribute('name', 'producto');

    id = `producto-${counter}`
    
    // label = document.createElement('label');
    // label.setAttribute('for', id);
    // label.textContent = 'Producto:';
    // div.appendChild(label);

    let product = document.createElement('div');
    product.setAttribute('class', 'bold')
    product.setAttribute('id', id);
    product.setAttribute('name', 'producto');
    product.setAttribute('value', producto.selectedOptions[0].value);
    product.textContent = producto.selectedOptions[0].textContent;
    div.appendChild(product);
    item.appendChild(div);

    /* Tipo producto */
    div = document.createElement('div');
    div.setAttribute('name', 'tipo');

    id = `tipo-${counter}`

    label = document.createElement('label');
    label.setAttribute('for', id);
    label.textContent = 'Tipo:'
    div.appendChild(label);

    // antes de clonar, hay que sacar el valor
    let valor = tipo.value;
    let type = tipo.cloneNode(true);
    type.setAttribute('id', id);
    for (var i, j = 0; i = type.options[j]; j++){
        if (i.value === valor){
            type.selectedIndex = j;
            break;
        }
    }
    div.appendChild(type);
    item.appendChild(div);

    /* Cantidad */
    div = document.createElement('div');
    div.setAttribute('name', 'cantidad');

    id = `cantidad-${counter}`;

    label = document.createElement('label');
    label.setAttribute('for', id);
    label.textContent = 'Cantidad:'
    div.appendChild(label);
    
    let quantity = cantidad.cloneNode(true);
    quantity.setAttribute('id', id);
    // quantity.setAttribute('name', 'quantity'); //cloned
    // quantity.setAttribute('class', 'short-input'); //cloned
    div.appendChild(quantity);
    item.appendChild(div);

    /* Precio del producto */
    div = document.createElement('div');
    div.setAttribute('name', 'precio');

    id = `precio-${counter}`

    label = document.createElement('label');
    label.setAttribute('for', id);
    label.textContent = 'Costo: ';
    div.appendChild(label);

    let price = document.createElement('div');
    price.setAttribute('name', 'precio');
    price.setAttribute('id', id);
    await changePrecio(product, type, price);
    div.appendChild(price);
    item.appendChild(div);

    /* Subtotal */
    div = document.createElement('div');
    div.setAttribute('name', 'subtotal');

    id = `subtotal-${counter}`;

    label = document.createElement('label');
    label.setAttribute('for', id);
    label.textContent = 'Subtotal:';
    div.appendChild(label);

    let subtotal = document.createElement('div');
    subtotal.setAttribute('name', 'subtotal');
    subtotal.setAttribute('id', id);
    changeSubtotal(price, cantidad, subtotal);
    div.appendChild(subtotal);
    item.appendChild(div);

    /* Eliminar */
    let eliminar = document.createElement('input');
    eliminar.type = 'button';
    eliminar.value = 'Eliminar';
    item.appendChild(eliminar);


    type.addEventListener('change', async function(){
        await changePrecio(product, type, price);
        changeSubtotal(price, quantity, subtotal);
    });

    quantity.addEventListener('change', function() {
        changeSubtotal(price, quantity, subtotal)
    });

    eliminar.addEventListener('click', function(){
        let total = document.getElementById('total');
        let substraction = parseFloat(subtotal.getAttribute('value'));
        total.value = parseFloat(total.value) - substraction;
        eliminar.parentNode.remove()
    });

    counter++;
    return item;
}

/**
 * Cambia el precio dependiendo del producto, tipo -> a la etiqueta precio
 */
function changeSubtotal(precio, cantidad, subtotal_label){
    let valor_precio = precio.textContent;
    let valor_cantidad = cantidad.value;
    let valor_subtotal;

    // Actualizar el total
    let total = document.getElementById('total');

    if (valor_cantidad && valor_precio){
        try {
            // $50
            valor_precio = parseFloat(valor_precio.slice(1));
            valor_cantidad = parseInt(valor_cantidad);
            valor_subtotal = valor_cantidad * valor_precio;

            if (valor_cantidad < 1 || isNaN(valor_cantidad)){
                console.error('Como q vas a sumar 0 o menos productos?')
                alert('No se puede usar cantidades negativas, letras o "0".')
                document.getElementById('comprar').disabled = true;
                return
            }
            document.getElementById('comprar').disabled = false;

            if (subtotal_label.getAttribute('value')){
                total.value = parseFloat(total.value) - parseFloat(subtotal_label.getAttribute('value'))
            }
            total.value = parseFloat(total.value) + valor_subtotal;
        } catch (error) {
            console.error('No se pudo convertir los valores: ', valor_cantidad, valor_precio, total.value);
            return;
        }
        

        subtotal_label.setAttribute('value', valor_subtotal);
        subtotal_label.textContent = `$${valor_subtotal}`;
    } else {
        console.error('No hay precio o cantidad');
        alert('Llena los campos de cantidad')
    }
}

/**
 * Cambia el precio dependiendo del producto, tipo -> a la etiqueta precio
 */
async function changePrecio(producto, tipo, precio){
    let data = await getPrice(producto, tipo);
    precio.setAttribute('value', data.id);
    precio.textContent = `$${data.precio}`;
}

/**
 * Actualiza los tipos disponibles según el producto
 */
function changeTipo(producto, tipo) {
    let id_producto = producto.value;

    let i = tipo.options.length;
    while (i > 0) tipo.remove(--i)

    fetch(`get-tipos-por-producto/${id_producto}`)
        // Si la promesa es buena, lo hacemos json
        .then( response => {
            return response.json();
        })
        // Leemos el json como data
        .then( data => {
            data.forEach(rowTipo => {
                var option = document.createElement('option');
                option.value = rowTipo.id_tipo_producto;
                option.textContent = rowTipo.tipo_producto;
                tipo.appendChild(option);
            });
        })
        .catch( error => console.error('Error al buscar tipos: ' + error));   
}

/**
 * Actualiza el precio según el producto y el tipo
 * @param {producto} producto el producto que viene con categoria
 * @param {tipo_producto} tipo_producto con el cual se relaciono el precio
 */
async function getPrice(producto, tipo_producto){
    let id_producto = producto.getAttribute('value');
    let id_tipo_producto = tipo_producto.value

    if (id_producto === undefined || id_tipo_producto === undefined){
        console.error('No se puede obtener el precio pq no existe')
        return;
    }
    try {
        const response = await fetch(`get-precio/${id_producto}&${id_tipo_producto}`);
        return await response.json();
    } catch (error) {
        return console.error('Error al buscar tipos: ' + error);
    }
}

/**
 * Envia las compras agregadas anteriormente al cart.
 * Crea un JSON con la información colectada por el cart
 */
function sendCart(){
    //Convertir a JSON
    let cart = document.getElementById('cart').children;
    let total = document.getElementById('total');
    let cartData = [];


    for (let item of cart){
        let c = item.children['cantidad'].children['cantidad'].value;
        let p = item.children['precio'].children['precio'].getAttribute('value');
        let s = item.children['subtotal'].children['subtotal'].getAttribute('value');
        
        let data = {
            cantidad: c,  //cantidad
            precio: p,      //precio
            subtotal: s  //subtotal
        };

        cartData.push(data);
    }

    let shop = {
        cart: cartData,
        total: total.value
    }

    //Enviar JSON
    fetch('nueva-venta', {
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
    let add_product = document.getElementById('agregar');
    let cart = document.getElementById('cart');

    //Informacion del producto
    let producto = document.getElementById('producto');
    let tipo = document.getElementById('tipo');
    let cantidad = document.getElementById('cantidad');
    let total = document.getElementById('total');

    let submit = document.getElementById('comprar')

    producto.value = '';
    tipo.value = '';
    cantidad.value = '';
    total.value = '0';

    let add_cart = async function(){
        if (producto.value === '' || tipo.value === '' || cantidad.value === ''){
            alert('Rellena los campos de PRODUCTO, TIPO PRODUCTO Y CANTIDAD');
            return;
        }

        if (parseInt(cantidad.value) < 1 || isNaN(parseInt(cantidad.value))){
            console.error('Como q vas a sumar 0 o menos productos?');
            alert('No se puede usar cantidades negativas, letras o el "0"');
            submit.disabled = true;
            return
        }

        submit.disabled = false;

        for (let i = 0; i < cart.children.length; i++){
            let p = document.getElementById(`producto-${i}`);
            let t = document.getElementById(`tipo-${i}`);

            // Si hay id-descontinuo
            if (!p && !t)
                continue;

            if (producto.value === p.getAttribute('value') && tipo.value === t.value){
                /* El producto ya existe en el carro, actualizamos */
                let c = document.getElementById(`cantidad-${i}`);
                let old_quant = c.value;
                try {
                    c.value = parseInt(old_quant) + parseInt(cantidad.value);
                } catch (error) {
                    console.error('No se pudo actualizar el producto con nueva info', error)
                    return;
                }
                changeSubtotal(document.getElementById(`precio-${i}`), c, document.getElementById(`subtotal-${i}`));
                return;
            }
        }

        /* Si no existe creamos la caja */
        let nueva_transaccion = await createBox(producto, tipo, cantidad);
        cart.prepend(nueva_transaccion);

        producto.value = '';
        tipo.value = '';
        cantidad.value = '';

    }
    
    add_product.addEventListener('click', async function(){
        await add_cart()
    });

    producto.addEventListener('change', function(){
        changeTipo(producto, tipo);
    });

    submit.addEventListener('click', function(){
        if (cart.children.length === 0)
            return;
        sendCart();
    });

    document.addEventListener('keyup', async function(e) {
        if (e.code === 'Enter')
            await add_cart()
    });
      
}

window.addEventListener('beforeunload', function (e) {
    var confirmationMessage = 'Are you sure you want to leave this page?';
    e.returnValue = confirmationMessage;  // Gecko, WebKit, Chrome <34
    return confirmationMessage;           // Gecko, WebKit, Chrome >=34
});

