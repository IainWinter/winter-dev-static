from file import ref, ref_page, read_file
from render_code import render_code
import latex2mathml.converter

def top(io):
	io.write(f'''
		<div class="top">
			<h1 class="title">Winter</h1>
			<div class="nav-section">
				<div class="nav-links">
					<a class="nav-link" href="{ref_page("articles")}">Articles</a>
					<a class="nav-link" href="{ref_page("projects")}">Projects</a>
					<a class="nav-link" href="{ref_page("support")}">Support</a>
				</div>

				<hr class="nav-separator" />

				<div class="nav-buttons">
					<img id="toggle-dark-icon" src="{ref("~/icons/light_off.svg")}" onclick="toggleDark();"/>
				</div>
			</div>
		</div>
		<script src="{ref("~/scripts/toggle_dark.js")}"></script>
	''')

def vars(io):
	io.write(f'''
		<script>
			const g_exportRootPath = "{ref("~/")}";
			function ref(path) {{ return g_exportRootPath + path; }}
		</script>
	''')

# article components

def sub_title(io, text):
	id = text.split(' ', 1)[0] # use first word as id

	io.write(f'''
		<h2 class="article-subtitle mark-section" id={id}>
			{text}
			<a class="article-subtitle-id-link" href="#{id}">#</a>
		</h2>
	''')

def sub_title2(io, text):
	return io.write(f'<h3>{text}</h3>')

def link(io, text):
	args = text.split(',', 1)
	name = args[0].strip()
	url = args[1].strip()

	# todo: put logic for if the url is referencing a local file

	io.write(f'<a class="underline" target="_blank" href="{ref(url)}">{name}</a>')

def iframe(io, src):
	io.write(f'<iframe class="article-embed" src="{ref(src)}"></iframe>')

# I wan't to be able to style the svg contents with the light/dark theme, but that can only happen if the svg is directly in the html
# so load it from a file and embed it
def svg(io, src):
	svg_contents = read_file(src)
	io.write(f'<div class="article-embed article-embed-no-height-limit">{svg_contents}</div>')

def svg_half(io, src):
	svg_contents = read_file(src)
	io.write(f'<div class="article-embed article-embed-no-height-limit article-embed-half">{svg_contents}</div>')

def image(io, src):
	io.write(f'<img class="article-embed" src="{ref(src)}"></img>')

def image_half(io, src):
	io.write(f'<img class="article-embed article-embed-half" src="{ref(src)}"></img>')

def iframe_youtube_video(io, src):
	# This is an iframe which is just an image, and on click gets replaces with the actual iframe
	# the images are stored under thumbnails/<youtube_id>.jpg
	# the youtube id is between the / and ? in the url

	# here is example js code const id = props.src.substring(props.src.lastIndexOf('/') + 1, props.src.indexOf('?'));

	youtube_id = src[src.rfind('/') + 1:src.find('?')]
	thumbnail_url = ref(f'~/thumbnails/{youtube_id}.jpg')
	iframe_src = f'https://www.youtube.com/embed/{youtube_id}?rel=0&modestbranding=1&autoplay=1'

	io.write(f'''
		<span class="article-embed article-embed-thumb-yt-icon">
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
			<pre class="article-code-text {language}">{code_dom_string}</pre>
		</div>
	''')

def equation(io, latex_text):
	mathml_output = latex2mathml.converter.convert(latex_text)

	io.write(f'''
		<div class="article-equation">
			{mathml_output}
		</div>
	''')

def equation_inline(io, latex_text):
	mathml_output = latex2mathml.converter.convert(latex_text)
	io.write(f'<span class="article-inline-equation">{mathml_output}</span>')

def br(io):
	io.write('<br />')

# names with _html are not direct functions, but ones that need inputs from the context

def comments_html(io, slug):
	io.write(f'''
		<div class="article-comment-section">
			<h2 class="article-subtitle mark-section" id="comments">Comments<a class="article-subtitle-id-link" href="#comments">#</a></h2>
			<br />
			<iframe id="comment-section-frame" class="comment-frame" scrolling="no" src="{ref(f'~/external/comments.html?host=https://api.winter.dev/comments&subject={slug}')}"></iframe>
			<script src="{ref("~/scripts/resize_comment_section.js")}"></script>
		</div>
	''')

def raw_html(io, text):
	io.write(text)

def title_html(io, text):
	io.write(f'<h1 class="page-title">{text}</h1>')

def card_html(io, meta, slug_href_root):
	slug = meta["slug"]
	title = meta["title"]
	date_str = meta["date"]
	href = meta.get("href", ref_page(f'{slug_href_root}/{slug}'))

	thumbnail_dom = ""
	
	if "thumbnail" in meta:
		thumbnail_src = ref(f'~/thumbnails/{meta["thumbnail"]}')
		thumbnail_dom = f'<a href={href}><img class="article-card-thumb" src="{thumbnail_src}" /></a>'

	io.write(f'''
		<div class="article-card">
			{thumbnail_dom}
			<div class="article-card-text">
				<a class="article-card-text-link" href={href}>{title}</a>
				<p class="article-card-text-date">{date_str}</p>
			</div>
		</div>
	''')

def card_list_html(io, page, context):
	cards = [context[slug] for slug in page["cards"]]

	cards_with_thumbnails = []
	cards_without_thumbnails = []

	for card in cards:
		if "thumbnail" in card:
			cards_with_thumbnails.append(card)
		else:
			cards_without_thumbnails.append(card)
	
	io.write('<div>')

	for card in cards_with_thumbnails:
		card_html(io, card, page["slug"])

	if len(cards_without_thumbnails) > 0:
		io.write('<hr class="article-cards-separator" />')

		for card in cards_without_thumbnails:
			card_html(io, card, page["slug"])

	io.write('</div>')

# mesh project components

def shape_card_html(io, shape):
	href = ref_page(f'projects/{shape["slug"]}')

	io.write(f'''
		<div class="shape">
			<div id="{shape["id"]}"></div>
			<a class="shape-title" href="{href}">{shape["title"]}</a>
			<div id="{shape["id"]}-tools"></div>
		</div>
	''')

def shapes_html(io, shape_names, context):
	for shape_name in shape_names:
		shape_card_html(io, context[shape_name])


def shape_title_html(io, title):
	io.write(f'<h1 class="page-title"><a href="{ref_page("/projects/mesh")}">Mesh</a> / {title}</h1>')

def shape_tools_html(io, shape):
	io.write(f'''
		<div id="{shape["id"]}"></div>
		<div id="{shape["id"]}-tools"></div>
	''')
	#<h3 class="shape-side-panel-name">{shape["title"]}</h3>
	#<table id="shape-table" class="shape-side-panel-table"></table>