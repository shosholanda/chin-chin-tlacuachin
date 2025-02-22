/**
 * Modulo de funciones para hacer cosas con elementos HTML
 * Podemos usar la variable CCT en cualquier archivo de javascript
 * para poder reutilizar el código.
 *
 * CCT = Chin Chin Tlacuachin
 */

var CCT = (function (CCT) {

	class HTML {


        static getSelectedValue(selectHTML){
            if (selectHTML && selectHTML.options != [])
                return selectHTML.options[selectHTML.selectedIndex].text;
            console.error("No se pudo seleccionar un valor");
            return null;
        }

        static addList(uList, value, text) {
            let li = document.createElement('li');
            li.setAttribute('value', value);
            li.addEventListener('click', function () {
                let suggestions = document.getElementById('suggestions');
                suggestions.innerHTML = "";
                let ul = document.getElementById('lista-insumos');
                console.log(value);
                let li = `  <li id="insumo-${value}">
          <a href="{{ url_for('inventario.articulo', id_articulo='VALUE')}}">${text} </a>
          <button onclick="eliminaInsumo(${value})">Eliminar</button>
        </li>`
                li = li.replace('VALUE', value);
                // console.log(li) Debe haber una mejor
        
                ul.insertAdjacentHTML('beforeend', li);
                suggestions.innerHTML = "";
            });
            li.textContent = text
            uList.appendChild(li);
        }
	}

	CCT.HTML = HTML;
	return CCT;

})(CCT || {})
