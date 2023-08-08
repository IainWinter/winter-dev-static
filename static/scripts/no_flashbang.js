let theme = localStorage.getItem("theme");

if (theme === null) {
	theme = "dark";
	localStorage.setItem("theme", theme);
}

window.document.documentElement.setAttribute("color-theme", theme);

function toggleDark() {
	theme = theme == "dark" ? "light" : "dark";
	window.document.documentElement.setAttribute("color-theme", theme);
	localStorage.setItem("theme", theme);
}