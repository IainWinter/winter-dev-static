from render_article import render_article
from render_code import render_code
from render_template import render_template

def render_winter_dev_article(template_text: str, article_text: str) -> str:
	def title(io, text):
		io.write(f'<h1 class="page-title">{text}</h1>')

	def sub_title(io, text):
		id = text.split(' ', 1)[0] # use first word as id

		io.write(f'''
			<h2 class="article-subtitle mark-section" id={id}>
				{text}
				<a class="article-subtitle-id-link" href="#{id}">#</a>
			</h2>
		''')

	def link(io, text):
		args = text.split(',', 1)
		name = args[0].strip()
		url = args[1].strip()
		io.write(f'<a class="underline" target="_blank" href="{url}">{name}</a>')

	def iframe(io, src):
		io.write(f'<iframe class="article-embed" src="{src}"></iframe>')

	def svg(io, src):
		# I wan't to be able to style the svg contents with the light/dark theme, but that can only happen if the svg is directly in the html
		# so load it from file and embed it
		
		with open(src, 'r') as f:
			svg_contents = f.read() # may be able to write directly to io
			io.write(f'<div class="article-embed">{svg_contents}</div>')

	def image(io, src):
		io.write(f'<img class="article-embed" src="{src}"></img>')

	def iframe_youtube_video(io, src):
		# This is an iframe which is just an image, and on click gets replaces with the actual iframe
		# the images are stored under thumbnails/<youtube_id>.jpg
		# the youtube id is between the / and ? in the url

		# here is example js code const id = props.src.substring(props.src.lastIndexOf('/') + 1, props.src.indexOf('?'));

		youtube_id = src[src.rfind('/') + 1:src.find('?')]
		thumbnail_url = f'/thumbnails/{youtube_id}.jpg'
		iframe_src = f'https://www.youtube.com/embed/{youtube_id}?rel=0&modestbranding=1&autoplay=1'

		io.write(f'''
			<span class="article-embed article-embed-thumb-wrap">
				<img class="article-embed-thumb" src="{thumbnail_url}" onclick="swapIframe(this, '{iframe_src}')"></img>
			</span>
		''')

	def code(io, arguments):
		args = arguments.split(',', 2)
		filename = args[0].strip()
		language = args[1].strip()
		code_template = args[2]

		code_dom_string = render_code(code_template, language)
		title_dom_string = "" if filename[-1] == '_' else f'<p class="article-code-file mark-section">{filename}</p>'

		io.write(f'''
			<div class="article-code draw-left-line">
				{title_dom_string}
				<pre class="{language}">{code_dom_string}</pre>
			</div>
		''')

	def placeholder(io, src):
		io.write(f'<placeholder>')

	article_funcs = {
		"title": title,
		"sub-title": sub_title,
		"link": link,
		"img": image,
		"svg": svg,
		"iframe": iframe,
		"iframe-youtube-video": iframe_youtube_video,
		"code": code,

		"equation": placeholder,
	}

	blocks, meta = render_article(article_text, article_funcs)

	def put(io, what):
		if what == "title":
			io.write(meta["title"])
		elif what == "article":
			for block in blocks:
				io.write(block)

	template_funcs = {
		"put": put
	}

	return render_template(template_text, template_funcs)