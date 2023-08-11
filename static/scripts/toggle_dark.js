const g_lightOnIcon = ref("icons/light_on.svg");
const g_lightOffIcon = ref("icons/light_off.svg");

const g_listenForThemeChange = []

function subscribeToThemeChange(func) {
	g_listenForThemeChange.push(func);
}

function toggleDark() {
	let theme = localStorage.getItem("theme");
	let icon = document.getElementById("toggle-dark-icon");

	if (theme == "dark") {
		theme = "light";
		icon.src = g_lightOnIcon;
	}
	else {
		theme = "dark";
		icon.src = g_lightOffIcon;
	}

	window.document.documentElement.setAttribute("color-theme", theme);
	localStorage.setItem("theme", theme);

	for (let func of g_listenForThemeChange)
		func(theme);
}

function setInitialIcon() {
	let theme = localStorage.getItem("theme");
	let icon = document.getElementById("toggle-dark-icon");

	icon.src = theme == "dark" ? g_lightOffIcon : g_lightOnIcon;
}

setInitialIcon();