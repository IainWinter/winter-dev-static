let g_frame = document.getElementById("comment-section-frame");
let g_commentTitle = document.getElementById("comments");

function childMessageHandler(e) {
	switch (e.data.reason) {
		case "setHeight":
			g_frame.height = e.data.height;
			break;
		case "askTheme":
			g_frame.contentWindow?.window.postMessage({ theme: localStorage.getItem("theme") }, "*");
			break;
		case "setScrollToComments":
			g_commentTitle.scrollIntoView();
			break;
	}
}

window.addEventListener("message", childMessageHandler);

subscribeToThemeChange((theme) => {
	g_frame.contentWindow?.window.postMessage({ theme: theme }, "*");
});