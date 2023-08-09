function swapIframe(img, iframeSrc) {
	// swap img for an iframe with its source set to iframeSrc
	// this is used to swap the thumbnail for a youtube embed

	var iframe = document.createElement("iframe");
	iframe.classList = "article-embed";
	iframe.src = iframeSrc;

	img.parentNode.appendChild(iframe);
	img.parentNode.classList = "article-embed";
	iframe.after(img);
	img.remove();
}