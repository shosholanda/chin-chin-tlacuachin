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
		static async fetch({url = "/", data = {}, type = 'GET'} = {}) {
			let request = {
				method: type,
				headers: {
					'Content-Type': 'application/json'
				}
			}

			if (type === 'POST' || type === 'PUT' || type === 'PATCH')
				request.body = JSON.stringify(data);
			
			let response = await fetch(url, request);
			console.log(request)
			if (!response.ok)
				throw new Error(`HTTP error! status: ${response.status}`);

			const contentType = response.headers.get('Content-Type');

			if (contentType && contentType.includes('application/json'))
				return await response.json();
			if (contentType && contentType.includes('text/html')){
				return {'html': await response.text(), 'url': response.url};
			}
			return response;
		}
	}

	CCT.Request = Request;
	return CCT;

})(CCT || {})
