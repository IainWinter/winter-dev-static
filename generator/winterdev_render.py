from winterdev_components import *
from text_renderer import *

# article
# article list
# project list
# project home page
# mesh project page

def winterdev_render_content(content: str):
	content_render = render_article(content, {
		"title": title_html,
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
	})

	return content_render

def winterdev_render_card_list(template: str, slug: str, context: dict) -> str:
	page = context[slug]
	
	render = render_template(template, {
		"card-list-title": lambda io: title_html(io, page["title"]),
		"card-list": lambda io: card_list_html(io, page, context),
		"name": lambda io: raw_html(io, page["title"]),
		"vars": vars,
		"top": top,
	})

	return render

def winterdev_render_article(template: str, slug: str, context: dict) -> str:
	page = context[slug]

	content_render = winterdev_render_content(page["content"])

	render = render_template(template, {
		"article": lambda io: raw_html(io, content_render),
		"name": lambda io: raw_html(io, page["title"]),
		"vars": vars,
		"top": top,
	})

	return render

def winterdev_render_project_simple(template: str, slug: str, context: dict) -> str:
	page = context[slug]

	render = render_template(template, {
		"project": lambda io: raw_html(io, page["content"]),
		"name": lambda io: raw_html(io, page["title"]),
		"title": lambda io: title_html(io, page["title"]),
		"vars": vars,
		"top": top,
	})

	return render

def winterdev_render_project_mesh_page_home(template: str, slug: str, context: dict) -> str:
	page = context[slug]

	content_render = render_template(page["content"], {
		"shapes": lambda io: shapes_html(io, page["shapes"], context)
	})

	render = render_template(template, {
		"project": lambda io: raw_html(io, content_render),
		"name": lambda io: raw_html(io, page["title"]),
		"title": lambda io: title_html(io, page["title"]),
		"vars": vars,
		"top": top,
	})

	return render

def winterdev_render_project_mesh_page_mesh(template: str, slug: str, context: dict) -> str:
	page = context[slug]

	content_render = winterdev_render_content(page["content"])

	render = render_template(template, {
		"name": lambda io: raw_html(io, page["title"]),
		"id": lambda io: raw_html(io, page["id"]),
		"shape-article": lambda io: raw_html(io, content_render),
		"shape-title": lambda io: shape_title_html(io, page["title"]),
		"shape-tools": lambda io: shape_tools_html(io, page),
		"vars": vars,
		"top": top,
	})

	return render