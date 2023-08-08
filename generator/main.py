from winterdev_generator import render_winter_dev_single_article, render_winter_dev_article_list

def create_rendered_single_article_file(template_file, article_file, out_file):
	template_text = ''
	with open(template_file, 'r', encoding='utf-8') as f:
		template_text = f.read()

	article_test = ''
	with open(article_file, 'r', encoding='utf-8') as f:
		article_test = f.read()

	out = render_winter_dev_single_article(template_text, article_test)
	with open(out_file, 'w', encoding='utf-8') as f:
		f.write(out)

def create_rendered_article_list_file(template_file, out_file):
	template_text = ''
	with open(template_file, 'r', encoding='utf-8') as f:
		template_text = f.read()

	out = render_winter_dev_article_list(template_text)
	with open(out_file, 'w', encoding='utf-8') as f:
		f.write(out)

create_rendered_single_article_file('../content/single_article_template.html', '../content/articles/epa-algorithm.md', '../static/articles/epa-algorithm.html')
create_rendered_article_list_file('../content/article_list_template.html', '../static/articles.html')