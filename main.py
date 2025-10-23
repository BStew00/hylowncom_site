import markdown
from markdown.extensions.toc import TocExtension
import argparse
import os
import frontmatter
import re


# text = "This is some text {remove this part} and this should stay."
# # Use re.sub to remove the curly-braced text
# cleaned_text = re.sub(r'\{[^}]*\}', '', text)
#
# This is some text  and this should stay.

# text = """# This is a level 1 header
# ## This is a level 2 header
# ### This is a level 3 header
# Some other text
# ## Another level 2 header"""
# 
# # Find lines that start with exactly two #
# lines_with_two_hashes = re.findall(r'^##[^#].*', text, re.M)
# 
# print(lines_with_two_hashes)
#
# ['## This is a level 2 header', '## Another level 2 header']


# def has_duplicates(lst):
#     return len(lst) != len(set(lst))
# 
# # Example usage
# numbers = [1, 2, 3, 2, 5]
# print(has_duplicates(numbers))  # Output: True   

# def find_duplicates_with_counts(lst):
#     count_dict = {}
#     for item in lst:
#         count_dict[item] = count_dict.get(item, 0) + 1
#     return {item: count for item, count in count_dict.items() if count > 1}
# 
# # Example usage
# items = ['apple', 'banana', 'apple', 'cherry', 'banana', 'banana']
# print(find_duplicates_with_counts(items))  # Output: {'apple': 2, 'banana': 3}  

# text = "Hello, World! 123 @#$%"
# # Remove all non-alphanumeric characters but leave spaces
# cleaned_text = re.sub(r'[^a-zA-Z0-9 ]', '', text) 

# text = "This   is    a    sentence    with   extra   spaces."
# # Replace all consecutive whitespace characters with a single space
# cleaned_text = re.sub(r'\s+', ' ', text)

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
    


# Get the filename of the md file
parser = argparse.ArgumentParser()
parser.add_argument(
    "file",
    help="Input file to process",
    nargs="?",
)
args = parser.parse_args()
prefix, _ = os.path.splitext(os.path.abspath(args.file))


# Get the YAML frontmatter; yaml is a dictionary
yaml = frontmatter.load(os.path.abspath(args.file))


def make_html(md: str, prefix: str) -> str:
    if "title" in yaml:
        tit = yaml['title']
    else:
        tit = prefix
    if "id_to_make_active" in yaml:
        activate = yaml['id_to_make_active']
    else:
        activate = ''
    if "source" in yaml:
        source = yaml['source']
    else:
        activate = ''
    with open(yaml['html_template'], 'r', encoding="utf-8") as htmltemplatefp:
        html_template = htmltemplatefp.read()
    mdbody = markdown.markdown(md, extensions=["smarty", "abbr", "attr_list", "fenced_code", "toc", "admonition", "tables"])
    tocst = make_toc(md)
    print(tocst)
    return html_template.format(title=tit, toc=tocst, body=mdbody, activate=activate, source=source)


# Read the MD file and store its contents as md
# frontmatter.load().content strips the YAML header
with open(args.file, 'r', encoding="utf-8") as mdfp:
    md = frontmatter.load(mdfp).content

# Convert the MD to HTML
html = make_html(md, prefix=prefix)

# Write the HTML file
with open(prefix + ".html", "w", encoding="utf-8") as htmlfp:
    htmlfp.write(html)
