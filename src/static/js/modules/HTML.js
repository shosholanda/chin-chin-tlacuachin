/**
 * Modulo de funciones para hacer cosas con elementos HTML
 * Podemos usar la variable CCT en cualquier archivo de javascript
 * para poder reutilizar el código.
 *
 * CCT = Chin Chin Tlacuachin
 */

var CCT = (function (CCT) {

    class HTML {

        static get(name, type='id'){
            if (type === 'id')
                return document.getElementById(name);
            if (type === 'name')
                return document.getElementsByName(name);
            if (type === 'tag')
                return document.getElementsByTagName(name);
            if (type === 'class')
                return document.getElementsByClassName(name);
        }


        static getSelectedValue(selectHTML) {
            if (selectHTML.constructor === String)
                selectHTML = document.getElementById(selectHTML);
            if (selectHTML && selectHTML.options != [])
                return selectHTML.options[selectHTML.selectedIndex];
            console.error("No se pudo seleccionar un valor");
            return null;
        }

        static getRadioValue(radioContainer){
            let element;
            if (radioContainer.constructor === String)
                element = document.getElementById(radioContainer);
            else element = radioContainer
            
            let options = element.getElementsByTagName('input');
            for (let option of options)
                if (option.checked)
                    return option;
            return null;
        }

        static cleanInnerHTML(HTMLelement){
            let element;
            if (HTMLelement.constructor === String)
                element = document.getElementById(HTMLelement);
            else element = HTMLelement
            element.innerHTML = "";
        }

        /**
         * Crea un elemento de html con sus atributos y funcion si existe.
         * @param {*} tag 
         * @param {*} attibutes 
         * @param {*} innerHTML 
         * @param {*} eventType 
         * @param {*} func 
         * @returns 
         */
        static createElement(tag, attibutes={}, innerHTML="", eventType="", func=null){
            let element = document.createElement(tag);
            for (const [key, value] of Object.entries(attibutes))
                element.setAttribute(key, value);
            element.innerHTML = innerHTML;
            if (eventType && func)
                element.addEventListener(eventType, func);
            return element;
        }

        static wrapElement({tag = 'div', attributes = {}}, ...elements){
            let wrapper = this.createElement(tag, attributes);
            for (let e of elements)
                wrapper.appendChild(e);
            return wrapper;
        }
    }

    CCT.HTML = HTML;
    return CCT;

})(CCT || {})
