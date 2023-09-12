function put_eq(id, eq) {
	let element = document.getElementById(id);
	if(element) {
		katex.render(String(eq), element);
	}
}