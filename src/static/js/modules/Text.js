/**
 * Modulo de funciones para manipular texto
 * Podemos usar la variable CCT en cualquier archivo de javascript
 * para poder reutilizar el código.
 *
 * CCT = Chin Chin Tlacuachin
 */

var CCT = (function (CCT) {

	class Text {

		static toTitleCase(str) {
			return str.replace(
				/\w\S*/g,
				text => text.charAt(0).toUpperCase() + text.substring(1)
					.toLowerCase()
			);
		}

		/* Selecciona las i primeras letras */
		static getFirstLetters(s, i = 2) {
			s = s.toUpperCase();
			if (s.length < 2) return "";
			if (s.length === 2) return s;
			return s.split(' ').map(w => {
				if (w.length <= 2)
					return ""
				return w.substring(0, i);
			}).join("");
		}


		/* Genera un código GTIN tipo PRODCATIPR */
		static generateCode(nombre="", categoria="", tipo_producto="", precio="") {
			nombre = this.getFirstLetters(nombre, 4)
			categoria = this.getFirstLetters(categoria)
			tipo_producto = this.getFirstLetters(tipo_producto)
			precio = precio
			return nombre + categoria + tipo_producto + precio;
		}

		static validateDefined(...obj){
			return obj.every(t => t !== undefined || t !== null);
		}

		static validateInt(...int){
			if (!this.validateDefined(int)) return false;
			if (int.constructor === Number) return int % 1 === 0;
			if (int.constructor === String) return !isNaN(parseInt(int)) 
			return int.every(t => (t === Number && t %1 !== 0) || !isNaN(parseInt(t)));
		}

		static validateDouble(...double){
			if (!this.validateDefined(int)) return false;
			if (double.constructor === Number) return true;
			if (double.constructor === String) return !isNaN(parseFloat(double)) 
			return double.every(t => t.constructor === Number || !isNaN(parseFloat(t)));
		}

		static validateString(...s){
			if (!this.validateDefined(int)) return false;
			if (s.constructor === Array)  return s.every(t =>  t.length >= 0);
			return s.every(t => t.constructor === String)
		}
	}

	CCT.Text = Text;
	return CCT;

})(CCT || {})
