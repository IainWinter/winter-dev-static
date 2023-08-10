from winterdev_generator import render_winter_dev_single_article, render_winter_dev_card_list, render_winter_dev_support
from file import read_file, write_file, set_export_root_dir, set_export_suffix_page_path, copy_changed_files
from os.path import isfile, join
import os
import sys

def generate_site(outdir, for_local):
	# load all article information into a list
	
	template_single_article = read_file('./content/single_article_template.html')
	template_card_list = read_file('./content/card_list_template.html')
	template_support = read_file('./content/support_template.html')

	article_folder = './content/articles/'
	article_list = []

	set_export_root_dir("../")

	if for_local:
		set_export_suffix_page_path(".html")

	for file in os.listdir(article_folder):
		file_path = join(article_folder, file)
		if isfile(file_path) and file_path.endswith('.md'):
			article_text = read_file(file_path)
			render = render_winter_dev_single_article(template_single_article, article_text)
			article_list.append(render)
	
	# write all articles to static/articles
	for (text, meta) in article_list:
		write_file(f'{outdir}/articles/{meta["slug"]}.html', text)
	
	articles_meta = [
		meta for (_, meta) in article_list
	]

	projects_meta = [
		{
			"title": "Subscriber Tracker",
			"date": "April 21, 2021",
			"thumbnail": "GLNI8zcn05c.jpg",
			"href": "https://winter.dev/stats/",
			"published": "True"
		},
		{
			"title": "Mesh Generation",
			"date": "October 3, 2020",
			"thumbnail": "prims.jpg",
			"href": "https://winter.dev/prims/",
			"published": "True"
		}
	]

	set_export_root_dir("./")

	articles_render = render_winter_dev_card_list(template_card_list, "Articles", articles_meta)
	projects_render = render_winter_dev_card_list(template_card_list, "Projects", projects_meta)
	support_render = render_winter_dev_support(template_support)

	# just make two files ez
	write_file(f'{outdir}/index.html', articles_render)
	write_file(f'{outdir}/articles.html', articles_render)
	write_file(f'{outdir}/projects.html', projects_render)
	write_file(f'{outdir}/support.html', support_render)

	copy_changed_files("./static", out_dir)

out_dir = sys.argv[1]
for_local = sys.argv[2] == "local"

generate_site(out_dir, for_local)