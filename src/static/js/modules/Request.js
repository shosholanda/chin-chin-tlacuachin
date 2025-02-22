/**
 * Modulo para manejar comunicación con el backend
 * Podemos usar la variable CCT en cualquier archivo de javascript
 * para poder reutilizar el código.
 *
 * CCT = Chin Chin Tlacuachin
 */

var CCT = (function (CCT) {

	class Request {

		/** Regresa lo que regresa el fetch con algunos ajustes automáticos */
		static async fetch({url = "/", data = {}, type = 'GET', redirect=null} = {}) {
			let request = {
				method: type,
				headers: {
					'Content-Type': 'application/json'
				}
			}
			
			if (redirect)
				request.redirect = redirect;

			if (type === 'POST' || type === 'PUT' || type === 'PATCH')
				request.body = JSON.stringify(data);
			// console.log(request);
			let response = await fetch(url, request);
			// console.log(response);

			if (response.type === 'opaqueredirect' || redirect === 'manual'){
				// No redireccionar automaticamente cuando hay flashes?
				window.location.href = response.url;
				if (type === 'GET'){
					// window.location.assign(response.url) // WTF solo en unos enpoints jala?
					// Sin esta linea salen dobles los mensajes de flash, pero redirigido correctamente
					window.location.reload();
				}
				return;
			}
			
			if (!response.ok)
				throw new Error(`HTTP error! status: ${response.status}`);

			const contentType = response.headers.get('Content-Type');

			if (contentType && contentType.includes('application/json'))
				return response.json();
			if (contentType && contentType.includes('text/html'))
				return response.text();
			
			return response;
		}
	}

	CCT.Request = Request;
	return CCT;

})(CCT || {})
