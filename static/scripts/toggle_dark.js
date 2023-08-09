function toggleDark() {
	let theme = localStorage.getItem("theme");
	let icon = document.getElementById("toggle-dark-icon");

	if (theme == "dark") {
		theme = "light";
		icon.src = "/light_on.svg";
	}
	else {
		theme = "dark";
		icon.src = "/light_off.svg";
	}

	window.document.documentElement.setAttribute("color-theme", theme);
	localStorage.setItem("theme", theme);
}

function setInitialIcon() {
	let theme = localStorage.getItem("theme");
	let icon = document.getElementById("toggle-dark-icon");

	icon.src = theme == "dark" ? "/light_off.svg" : "/light_on.svg";
}

setInitialIcon();