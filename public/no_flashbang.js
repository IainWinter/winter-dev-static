// The the default theme is statically generated to be dark

let theme = "dark";

const noTheme = localStorage.getItem("theme") === null;

if (noTheme) localStorage.setItem("theme", theme);
else         theme = localStorage.getItem("theme");

window.document.documentElement.setAttribute("color-theme", theme);