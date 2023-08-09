const g_lightOnIcon = ref("light_on.svg");
const g_lightOffIcon = ref("light_off.svg");

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
}

function setInitialIcon() {
	let theme = localStorage.getItem("theme");
	let icon = document.getElementById("toggle-dark-icon");

	icon.src = theme == "dark" ? g_lightOffIcon : g_lightOnIcon;
}

setInitialIcon();