/**
 * Modulo para reutilizar código para eventos con elementos HTML/CSS
 * Podemos usar la variable CCT en cualquier archivo de javascript
 * para poder reutilizar el código.
 *
 * CCT = Chin Chin Tlacuachin
 */

var CCT = (function (CCT) {

	class Event {

        static changeVisibility(elementId, type='block'){
            let element = document.getElementById(elementId);
            let display = element.style.display;
            // console.log(display)
            if (element){
                if (display === 'none' || display === '')
                    element.style.display = type;
                else
                    element.style.display = 'none';
                return;
            }
            console.error("No se encontró el elemento", elementId);
        }

        static changeText(elementId, changeFor){

        }

        static changeDisabled(elementId, changeFor=null){
            let element = document.getElementById(elementId);
            if (element){
                if (changeFor)
                    element.disabled = changeFor;
                else
                    element.disabled = !element.disabled
                return;
            }
            console.error("No se encontró el elemento", element)
        }
	}

	CCT.Event = Event;
	return CCT;

})(CCT || {})
