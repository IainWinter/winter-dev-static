import os
import shutil
import filecmp

def read_file(path):
	text = ''
	with open(path, 'r', encoding='utf-8') as f:
		text = f.read()
	return text

def write_file(path, text):
	print(f'Wrote {path}')
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w', encoding='utf-8') as f:
		f.write(text)

def copy_changed_files(source_dir, target_dir):
	for root, _, files in os.walk(source_dir):
		for file in files:
			source_path = os.path.join(root, file)
			target_path = os.path.join(target_dir, os.path.relpath(source_path, source_dir))

			if not os.path.exists(target_path) or not filecmp.cmp(source_path, target_path):
				os.makedirs(os.path.dirname(target_path), exist_ok=True)
				shutil.copy2(source_path, target_path)
				print(f"Copied: {source_path} -> {target_path}")

#
# file cache
#

g_filecache = {}

def read_file_cached(filepath):
	if filepath not in g_filecache:
		file_contents = read_file(filepath)
		g_filecache[filepath] = file_contents 
	
	return g_filecache[filepath]

# use a global config for linking files
# based on if this should be a local export that can link files correctly when exported as file://
# or the site is exported to a site with the root at /
# or for github pages the site is exported with a root which is not /, but a random subfolder# this 

g_export_root_dir = ""
g_export_suffix_page_path = ""

def set_export_root_dir(export_root_dir: str):
	global g_export_root_dir
	g_export_root_dir = export_root_dir

def set_export_suffix_page_path(export_suffix_page_path: str):
	global g_export_suffix_page_path
	g_export_suffix_page_path = export_suffix_page_path

# I was using join, but it converts ./ to / which is not what I want to do

# If path starts with ~/ then it is relative to the export root dir
# else just return the path unchanged
def ref(path):
	if path.startswith('~/'):
		return f'{g_export_root_dir}{path[2:]}' 
		
	return path

def ref_page(path):
	return f'{g_export_root_dir}{path}{g_export_suffix_page_path}'