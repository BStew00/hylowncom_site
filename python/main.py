# Run this file from project's root directory

import markdown
import os
import sys
from pathlib import Path
import argparse
import frontmatter
import re
import shutil



# # List all files in directory "dir"
# def file_list(dir):
#     return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]



# Get all the level 2 headers into a list
# Remove # and {...} and non-alpha-numeric characters
# Trim leading and trailing whitespace and convert double spaces to single spaces
# Replace spaces with -
# Check for duplicates
# If duplicates exist, append _i for i=1,2,... to all but the first
# Add the html code
# Convert to a multi-line string
def make_toc(md: str) -> str:
    titles = re.findall(r'^##[^#].*', md, re.M) # Get all H2
    ids = []
    for i in range(len(titles)):
        t = titles[i]
        t = re.sub(r'\{[^}]*\}', '', t) # remove curly-braced-material, e.g. class definitions
        t = re.sub(r'#+', '', t)
        titles[i] = t.strip()
        t = re.sub(r'[^a-zA-Z0-9 ]', '', t) # remove non-alpha-numeric
        t = t.strip() # remove leading and trailing spaces
        t = re.sub(r'\s+', ' ', t) # replace multiple spaces with just one
        t = re.sub(r'\s', '-', t) # replace space with -
        ids.append(t.lower())
    if (len(ids) != len(set(ids))): # If duplicates
        out, cnt = [], {}
        for d in ids:
            if d not in cnt:
                cnt[d] = 1
            else:
                cnt[d] += 1
                d = d + "_{}".format(cnt[d]-1)
            out.append(d)
    else:
        out = ids
    lines = []
    for i in range(len(ids)):
        lines.append('<li class="template__nav-item"><a href="#' + out[i] + '">' + titles[i] + '</a></li>')
    return "\n".join(lines)





def make_html(md: str, f:Path) -> str:
    prefix = os.path.join(os.getcwd(), 'source')
    rootbk = "zero"
    if str(f).count("\\")>1:
        rootbk = "../"*(str(f).count("\\")-1*(f.stem.lower()=="index"))
    tit = ''
    active = ''
    github_source = ''
    pagetoc = ''
    if "title" in yaml:
        tit = yaml['title']
    if "id_to_make_active" in yaml:
        active = yaml['id_to_make_active']
    if "source" in yaml:
        sourceval = str(yaml["source"])
        if sourceval.lower() == "true":
                x = re.sub("source", "", str(f))
                x = re.sub(r"\\", "/", x)
                github_source_prefix = "https://raw.githubusercontent.com/BStew00/hylowncom_site/main"
                github_source = github_source_prefix + x
                print("source added: " + github_source)
        else:
            print("value of 'source' in yaml header was " + sourceval + ", no source added.")
    else:
        print("no 'source' in yaml header; no source added.")
    with open(os.path.join(prefix, yaml['html_template']), 'r', encoding="utf-8") as htmltemplatefp:
        html_template = htmltemplatefp.read()
    pagetoc = make_toc(md)
    if "page_type" in yaml:
        type = str(yaml["page_type"])
        if type.lower() == "homepage":
          return html_template
    mdbody = markdown.markdown(md, extensions=["smarty", "abbr", "attr_list", "fenced_code", "toc", "admonition", "tables"])
    if "{root}" in mdbody:
        mdbody = mdbody.format(root=rootbk)
    return html_template.format(
        title=tit, toc=pagetoc, body=mdbody, 
        activate=active, source=github_source,
        root=rootbk
        )




# List all subdirectories in directory "dir"
def dir_list(dir):
    return [item for item in os.listdir(dir) if os.path.isdir(os.path.join(dir,item))]




# List of subdirectories in project root
rootdirs  = dir_list('.')

# Exit if subdirectory 'source' doesn't exist
if "source" not in rootdirs:
    sys.exit(f"ERROR: no directory named 'source' in " + os.getcwd())

# Create directory 'site' if it doesn't exist
if "site" not in rootdirs:
    os.mkdir("site")
    print("Created directory 'site'")
else:
    print("Building the site in existing directory 'site'")


#print(dir_list("source"))
#print(file_list("source"))
#print(file_list("source/homelab"))
#print(os.listdir('source'))
#flst = file_list("source")



# Create the directories
sourcefp = os.path.join(os.getcwd(), "source")
sitefp = os.path.join(os.getcwd(), "site")
for dirpath, dirnames, filenames in os.walk(sourcefp):
    structure = os.path.join(sitefp, os.path.relpath(dirpath, sourcefp))
    if not os.path.isdir(structure):
        os.mkdir(structure)
        print('Created: ' + structure)
    else:
        print(structure + " already exits.")

# List of all MD files in source/
mdlst = [f for f in Path("source").rglob("*.md")]
#mdlstshort = mdlst[0:2]
for f in mdlst:
    print("############\n############")
    print("working on " + str(f) + " ...")
    # Read the MD file and store its contents as md
    # frontmatter.load().content strips the YAML header
    with open(f, 'r', encoding="utf-8") as mdfp:
      md = frontmatter.load(mdfp).content
    # Get the YAML frontmatter; yaml is a dictionary
    yaml = frontmatter.load(os.path.abspath(f))
    # Convert the MD to HTML
    html = make_html(md, f)
    # Write the HTML files
    writefp = Path(re.sub("source", "site", str(f), count=1))
    writefp = writefp.with_suffix(".html")
#    print(str(writefp.stem).lower() != "index")
#    print(not os.path.isdir(os.path.splitext(writefp)[0]))
#    print(os.path.splitext(writefp)[0])
#    print(os.path.join(os.path.splitext(writefp)[0], "index.html"))
#    print(writefp.stem)
    if str(writefp.stem).lower() != "index":
        if not os.path.isdir(os.path.splitext(writefp)[0]):
            os.mkdir(os.path.splitext(writefp)[0])
        writefp = os.path.join(os.path.splitext(writefp)[0], "index.html")
    with open(writefp, "w", encoding="utf-8") as htmlfp:
      htmlfp.write(html)
    print("Created: " + str(writefp))
    #print()
