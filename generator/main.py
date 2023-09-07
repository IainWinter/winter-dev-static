from winterdev_generator import render_winter_dev_article, render_winter_dev_card_list, render_winter_dev_support, render_winter_dev_project
from file import read_file, write_file, set_export_root_dir, set_export_suffix_page_path, copy_changed_files
from os.path import isfile, join
import os
import sys

def generate_content_from_folder(content_folder, ends_with, template_func, template_text):
	text = []
	meta = []

	for file in os.listdir(content_folder):
		file_path = join(content_folder, file)
		if isfile(file_path) and file_path.endswith(ends_with):
			content_text = read_file(file_path)
			(t, m) = template_func(template_text, content_text)
			text.append(t)
			meta.append(m)
	
	return (text, meta)

def generate_site(outdir, for_local):
	template_single_article = read_file('./content/single_article_template.html')
	template_single_project = read_file('./content/single_project_template.html')
	template_card_list = read_file('./content/card_list_template.html')
	template_support = read_file('./content/support_template.html')

	article_folder = './content/articles/'
	project_folder = './content/projects/'

	if for_local:
		set_export_suffix_page_path(".html")

	set_export_root_dir("../")

	(article_list, article_meta) = generate_content_from_folder(article_folder, '.md', render_winter_dev_article, template_single_article)
	(project_list, project_meta) = generate_content_from_folder(project_folder, '.html', render_winter_dev_project, template_single_project)

	set_export_root_dir("./")

	articles_render = render_winter_dev_card_list(template_card_list, "Articles", "articles", article_meta)
	projects_render = render_winter_dev_card_list(template_card_list, "Projects", "projects", project_meta)
	support_render = render_winter_dev_support(template_support)

	# write all articles to ~/articles
	for (text, meta) in zip(article_list, article_meta):
		write_file(f'{outdir}/articles/{meta["slug"]}.html', text)	

	# write all projects to ~/projects
	for (text, meta) in zip(project_list, project_meta):
		write_file(f'{outdir}/projects/{meta["slug"]}.html', text)

	write_file(f'{outdir}/index.html', articles_render)        # default page is articles, just send a copy
	write_file(f'{outdir}/articles.html', articles_render)
	write_file(f'{outdir}/projects.html', projects_render)
	write_file(f'{outdir}/support.html', support_render)

	copy_changed_files("./static", out_dir)

out_dir = sys.argv[1]
for_local = sys.argv[2] == "local" if len(sys.argv) > 2 else False

generate_site(out_dir, for_local)