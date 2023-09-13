# what if instead of a bunch of stupid functions, one config file can be provided and lazy load the required
# files depending on the files that the user wants to write

from winterdev_render import *
from file import *

def render_page(page, context):
	# populate the context with the new info, maybe throw if already exists?
	meta = page["meta"]
	slug = meta["slug"]
	context[slug] = meta

	# load the content if it exists
	if "content" in page:
		content = read_file_cached(page["content"])
		context[slug]["content"] = content

	template = read_file_cached(page["template"])
	render_function = globals()[page["render"]]

	return render_function(template, slug, context)

def render_site(config):
	context = {} # this is the list of all metadata keyed on slug -> metadata

	set_export_suffix_page_path(config["file_ext"])

	for page in config["pages"]:
		page_outfile = page["outdir"] + page["meta"]["slug"]
		page_outdir = os.path.dirname(page_outfile)
		page_to_root = (os.path.relpath('./', page_outdir) + '/').replace('\\', '/')
		outfile = config["outdir"] + page_outfile + ".html" #config["file_ext"] 

		# files = []
		# files.append(page["template"])			

		# if not are_sources_new(outfile, [page["template"]]):
		# 	print(f"Skipped: {page_outfile}")
		# 	continue

		set_export_root_dir(page_to_root)
		render = render_page(page, context)

		write_file(outfile, render)

	copy_changed_files(config["staticdir"], config["outdir"])

#
# driver
#

config = {
	"file_ext": "",
	"outdir": "../published/",
	"staticdir": "./static/",
	"pages": [
		{
			"outdir": "articles/",
			"template": "./content/article_template.html",
			"content": "./content/articles/falling-sand-worlds.md",
			"render": "winterdev_render_article",
			"meta": {
				"slug": "falling-sand-worlds",
				"title": "Making an infinite world with Falling Sand part 2",
				"date": "March 27, 2021",
				"thumbnail": "vNcsPE_YdmA.jpg"
			}
		},
		{
			"outdir": "articles/",
			"template": "./content/article_template.html",
			"content": "./content/articles/falling-sand-simulations.md",
			"render": "winterdev_render_article",
			"meta": {
				"slug": "falling-sand",
				"title": "Making games with Falling Sand part 1",
				"date": "December 30, 2020",
				"thumbnail": "wZJCQQPaGZI.jpg"
			}
		},
		{
			"outdir": "articles/",
			"template": "./content/article_template.html",
			"content": "./content/articles/epa-algorithm.md",
			"render": "winterdev_render_article",
			"meta": {
				"slug": "epa-algorithm",
				"title": "EPA: Collision response algorithm for 2D/3D",
				"date": "November 17, 2020",
				"thumbnail": "0XQ2FSz3EK8.jpg"
			}
		},
		{
			"outdir": "articles/",
			"template": "./content/article_template.html",
			"content": "./content/articles/gjk-algorithm.md",
			"render": "winterdev_render_article",
			"meta": {
				"slug": "gjk-algorithm",
				"title": "GJK: Collision detection algorithm in 2D/3D",
				"date": "August 29, 2020",
				"thumbnail": "MDusDn8oTSE.jpg"
			}
		},
		{
			"outdir": "articles/",
			"template": "./content/article_template.html",
			"content": "./content/articles/physics-engine.md",
			"render": "winterdev_render_article",
			"meta": {
				"slug": "physics-engine",
				"title": "Designing a physics engine",
				"date": "July 31, 2020",
				"thumbnail": "-_IspRG548E.jpg"
			}
		},
		{
			"outdir": "articles/",
			"template": "./content/article_template.html",
			"content": "./content/articles/another-way.md",
			"render": "winterdev_render_article",
			"meta": {
				"slug": "another-way",
				"title": "Another way of programming, taking it slow",
				"date": "July 6, 2020"
			}
		},
		{
			"outdir": "",
			"template": "./content/card_list_template.html",
			"render": "winterdev_render_card_list",
			"meta": {
				"slug": "articles",
				"title": "Articles",
				"cards": [
					"falling-sand-worlds",
					"falling-sand",
					"epa-algorithm",
					"gjk-algorithm",
					"physics-engine",

					"another-way",
				]
			}
		},

		# support page

		{
			"outdir": "",
			"template": "./content/support_template.html",
			"render": "winterdev_render_support",
			"meta": {
				"slug": "support"
			}
		},

		# subscriber project
		{
			"outdir": "projects/",
			"template": "./content/project_template.html",
			"content": "./content/projects/subscribers.html",
			"render": "winterdev_render_project_simple",
			"meta": {
				"slug": "subscribers",
				"title": "Subscriber Tracker",
				"date": "April 21, 2021",
				"thumbnail": "GLNI8zcn05c.jpg"
			}
		},

		# mesh project
		{
			"outdir": "projects/",
			"template": "./content/projects/mesh_pages/template.html",
			"content": "./content/projects/mesh_pages/plane.md",
			"render": "winterdev_render_project_mesh_page_mesh",
			"meta": {
				"slug": "mesh/plane",
				"title": "Plane",
				"id": "plane"
			}
		},
		{
			"outdir": "projects/",
			"template": "./content/projects/mesh_pages/template.html",
			"content": "./content/projects/mesh_pages/capsule.md",
			"render": "winterdev_render_project_mesh_page_mesh",
			"meta": {
				"slug": "mesh/capsule",
				"title": "Capsule",
				"id": "capsule"			
			}
		},
		{
			"outdir": "projects/",
			"template": "./content/projects/mesh_pages/template.html",
			"content": "./content/projects/mesh_pages/uvsphere.md",
			"render": "winterdev_render_project_mesh_page_mesh",
			"meta": {
				"slug": "mesh/uvsphere",
				"title": "UV Sphere",
				"id": "uvsphere"
			}
		},
		{
			"outdir": "projects/",
			"template": "./content/projects/mesh_pages/template.html",
			"content": "./content/projects/mesh_pages/icosphere.md",
			"render": "winterdev_render_project_mesh_page_mesh",
			"meta": {
				"slug": "mesh/icosphere",
				"title": "Icosphere",
				"id": "icosphere"
			}
		},
		{
			"outdir": "projects/",
			"template": "./content/project_template.html",
			"content": "./content/projects/mesh.html",
			"render": "winterdev_render_project_mesh_page_home",
			"meta": {
				"slug": "mesh",
				"title": "Mesh Generation Algorithms",
				"date": "April 21, 2021",
				"thumbnail": "prims.jpg",
				"shapes": [
					"mesh/plane",
					"mesh/capsule",
					"mesh/uvsphere",
					"mesh/icosphere",
				]
			}
		},

		{
			"outdir": "",
			"template": "./content/card_list_template.html",
			"render": "winterdev_render_card_list",
			"meta": {
				"slug": "projects",
				"title": "Projects",
				"cards": [
					"subscribers",
					"mesh"
				]
			}
		}
	]
}

render_site(config)