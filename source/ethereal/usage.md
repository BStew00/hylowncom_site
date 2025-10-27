---
title: Ethereal | Hylown
html_template: ethereal/hylowncom_ethereal.html
id_to_make_active: Usage
source: True
---

# How to Use <br>_Ethereal_ <strong style="color:#78b0a0">to</strong> Make Docs

Run `python/main.py` on Windows or Linux.  Tested on Windows 11 and Linux Debian bookworm; have not tested on MacOS.  

```
$ cd /path/to/project-root
$ python main.py
```

Or hit the run button in VScode.

Packages used:  

* [markdown](https://pypi.org/project/Markdown/)
* [os](https://docs.python.org/3/library/os.html)
* [sys](https://docs.python.org/3/library/sys.html)
* [pathlib](https://docs.python.org/3/library/pathlib.html)
* [frontmatter](https://pypi.org/project/python-frontmatter/)
* [re](https://docs.python.org/3/library/re.html)


## File structure {: class="template__section" }

Here's the file structure to use:

```
Ethereal-to-Make-Docs
├── python
├── site
│   └── assets
└── source
```

`project-root` is the name of your project.  `python/` houses `main.py`.  `site/` is created by `main.py` if it doesn't already exist.  `main.py` does not create the directory `assets/`; it is optional and you place it there with your CSS, Javascript, and other files.  `source/` contains all the Markdown source files of all your site's webpages.  

Example file structure for a site that has two "Books" (distinct areas of the website).  "Book 2" is just a single page.  "Book 1" has three "Chapters"; "Chapters" 1 & 3 are each only a single page, "Chapter 2" has a homepage and two additional pages.  

```
Ethereal-to-Make-Docs
├── .gitignore
├── LICENSE
├── README.md
├── python
│   └── main.py
├── site
│   └── assets
│       ├── css
│       │   ├── ethereal.css
│       └── javascript
│           └── ethereal.js
└── source
    ├── book1
    │   ├── book1.html
    │   ├── chapter2
    │   │   ├── index.md
    │   │   ├── page1.md
    │   │   └── page2.md
    │   ├── chapter3.md
    │   └── index.md
    ├── book2
    │   ├── book2.html
    │   └── index.md
    ├── ethereal.html
    └── index.md
```

After running `main.py` the site directory will look like this:

```
├── site
│   └── assets
│       ├── css
│       │   ├── ethereal.css
│       └── javascript
│           └── ethereal.js
├────── book1
│       ├── chapter2
│       │   ├── index.html
│       │   ├── page1
│       │   │   └── index.html
│       │   └── page2
│       │       └── index.html
│       ├── chapter3
│       │   └── index.html
│       └── index.html
├────── book2
│       └── index.html
└────── index.html
```

        

All the HTML files under `source/` are templates; all the HTML files under `site/` are those created by `main.py` using `python-markdown`.  Each directory's homepage should be named `index.md`.  



## python/main.py {: class="template__section" }

_Ethereal_ Uses `python-markdown` to render your Markdown files under `source/` to HTML files under `site/`.  It creates the correct directory structure under `site/` if it doesn't already exist, including the directory `site/` itself.  It does not create the `assets/` directory; this is where you customize by placing CSS, Javascript, and other files.

Since it uses `python-markdown` you should be able to use all the features of that package (only the ones used here have been tested).  

Your Markdown source files can have a YAML header to pass the following information to the python code:  

* Optional  
    * `page_type`:  
    If it has the case-insensitive value `homepage`, then `main.py` returns the HTML template; useful for website homepage.
    * `title`:  
    String passed to HTML template; use it for the `<title>` element in the `<head>`.
    * `id_to_make_active`:  
    HTML ID of the left TOC element for the page
    * `source`:  
    Boolean to determine whether to add the URL for the Markdown source on GitHub.
* Required if `page_type` is missing or is present and equals anything other than `homepage`
    * `html_template`:  
    Location from `project-root/` to the HTML template.


`main.py` uses the python format method to pass 6 values to the HTML template:

```python
return html_template.format(
    title    = tit, 
    toc      = pagetoc, 
    body     = mdbody, 
    activate = active, 
    source   = github_source,
    root     = rootbk
    )
```

The values of `tit` and `active` come directly from `title` and `id_to_make_active` YAML values, resp. The value of `pagetoc` is generated automaticaly from the H2 Headings.  The value of `mdbody` is everything in your Markdown source file below the YAML header.  The value of `github_source` will be created if the YAML value `source` is `true`.  

The value of `rootbk` is automatically generated, and represents the path back to `project-root` from the directory housing the current Markdown source file, e.g. we might have that `rootbk = "../../"`.  

In your HTML template write links using `{-root-}` **without the dashes**, e.g.

```
href="{-root-}assets/css/ethereal.css" <!-- Remove the dashes around -root-! -->
```

Can also be used in the Markdown source **without the dashes**, e.g.

```
![](-{root-}assets/my_image.png){: width=700 height=466}

** Remove the dashes around -root-! **
```


## .gitignore {: class="template__section" }

The `.gitignore` file has:

```
site/*
!site/assets/
!site/assets/**  
```

You don't want to copy your generated website, only the underlying code.  This .gitignore ignores everything in `site/` except  `assets/` and its contents.

