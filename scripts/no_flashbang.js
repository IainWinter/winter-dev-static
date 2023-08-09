function loadInitalCookieOrSetDefault() {
	let theme = localStorage.getItem("theme");
	
	if (theme === null) {
		theme = "dark"; // set the default theme to dark
		localStorage.setItem("theme", theme);
	}

	window.document.documentElement.setAttribute("color-theme", theme);
}

loadInitalCookieOrSetDefault();