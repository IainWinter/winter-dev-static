from render_article import render_article
from render_code import render_code
from render_template import render_template
import latex2mathml.converter
from os.path import join
from file import read_file, ref, ref_page

def title(io, text):
	io.write(f'<h1 class="page-title">{text}</h1>')

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

def ref_resource(io, path):
	io.write(ref(path))

def render_winter_dev_single_article(template_text: str, article_text: str) -> str:
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

	article_funcs = {
		"title": title,
		"sub-title": sub_title,
		"sub-title2": sub_title2,
		"link": link,
		"img": image,
		"img-half": image_half,
		"svg": svg,
		"svg-half": svg_half,
		"iframe": iframe,
		"iframe-youtube-video": iframe_youtube_video,
		"code": code,
		"equation": equation,
		"equation-inline": equation_inline,
		"br": br
	}

	blocks, meta = render_article(article_text, article_funcs)

	def name(io):
		io.write(meta["title"])
	
	def article(io):
		for block in blocks:
			io.write(block)

	def comments(io):
		io.write(f'''
			<div class="article-comment-section">
				<h2 class="article-subtitle mark-section" id="comments">Comments<a class="article-subtitle-id-link" href="#comments">#</a></h2>
				<br />
				<iframe id="comment-section-frame" class="comment-frame" scrolling="no" src="{ref(f'~/external/comments.html?subject={meta["slug"]}')}"></iframe>
				<script src="{ref("~/scripts/resize_comment_section.js")}"></script>
			</div>
	   ''')
		
	template_funcs = {
		"name": name,
		"article": article,
		"comments": comments,
		"top": top,
		"vars": vars,
		"ref": ref_resource,
	}

	rendered_text = render_template(template_text, template_funcs)

	return (rendered_text, meta)

def render_winter_dev_card_list(template_text: str, card_list_title: str, card_meta_list) -> str:
	def card(io, meta_data):
		if "published" not in meta_data or meta_data["published"] == "false":
			return

		if "title" not in meta_data:
			raise Exception("title is a required meta_data field")
		
		if "date" not in meta_data:
			raise Exception("date is a required meta_data field")
		
		slug_text = meta_data.get("slug", "")
		img_text = meta_data.get("thumbnail", "")

		slug_href = ref_page(f'articles/{slug_text}')
		thumb_href = ref(f'thumbnails/{img_text}')

		title_text = meta_data["title"]
		date_text = meta_data["date"]
		href_text = meta_data.get("href", slug_href)

		thumbnail_dom = ""

		if img_text != "":
			thumbnail_dom = f'<a href={href_text}><img class="article-card-thumb" src="{thumb_href}" /></a>'

		io.write(f'''
			<div class="article-card">
				{thumbnail_dom}
				<div class="article-card-text">
					<a class="article-card-text-link" href={href_text}>{title_text}</a>
					<p class="article-card-text-date">{date_text}</p>
				</div>
			</div>
		''')

	def card_list(io, meta_data_list):
		io.write('<div>')

		meta_data_with_thumbnails    = [meta_data for meta_data in meta_data_list if "thumbnail" in meta_data]
		meta_data_without_thumbnails = [meta_data for meta_data in meta_data_list if "thumbnail" not in meta_data]

		for meta_data in meta_data_with_thumbnails:
			card(io, meta_data)

		if len(meta_data_without_thumbnails) > 0:
			io.write('<hr class="article-cards-separator" />')

			for meta_data in meta_data_without_thumbnails:
				card(io, meta_data)

		io.write('</div>')
	
	def write_card_list_title(io):
		title(io, card_list_title)
	
	def write_card_list(io):
		card_list(io, card_meta_list)

	def name(io):
		io.write(card_list_title)

	template_funcs = {
		"top": top,
		"name": name,
		"card-list-title": write_card_list_title,
		"card-list": write_card_list,
		"vars": vars,
		"ref": ref_resource,
	}

	return render_template(template_text, template_funcs)

def render_winter_dev_support(template_test: str) -> str:
	template_funcs = {
		"top": top,
		"vars": vars,
		"ref": ref_resource,
	}

	return render_template(template_test, template_funcs)