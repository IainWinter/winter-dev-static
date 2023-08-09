let g_frame = document.getElementById("comment-section-frame");

// function setFrameTheme() {
// 	frame.current?.contentWindow?.window.postMessage({ theme: themeContext.theme }, "*");
// }

function childMessageHandler(e) {
	switch (e.data.reason) {
		case "setHeight":
			g_frame.height = e.data.height;
			break;
		case "askTheme":
			//setFrameTheme();
			break;
	}
}

window.addEventListener("message", childMessageHandler);