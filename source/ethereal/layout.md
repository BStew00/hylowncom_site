---
title: Ethereal | Hylown
html_template: ethereal/hylowncom_ethereal.html
id_to_make_active: Layout
source: True
---

# _Ethereal_ <strong style="color:#78b0a0">to</strong> Make Docs


## HTML/CSS Structure {: class="template__section" }

Responsive breakpoints are 

**phone** | `768px` | **tablet** | `1024px` | **laptop**

* Under 1024px Hamburger menu icon appears, left TOC hidden & moved to menu
* Under 768px right TOC hidden; current version of this template does not place it in menu



## Outline {: class="template__section" }

Here is how _Ethereal_'s main HTML elements are arranged.  

- html
- head
- body -- ``flex, column``
    - header
    - .container -- ``flex, column``
        - main
            - .main__inner .grid ``flex, row``
                - .sidebar .sidebar--primary
                    - .sidebar__scrollwrap
                        - .sidebar__inner
                - .sidebar .sidebar--secondary
                    - .sidebar__scrollwrap
                      - .sidebar__inner
                - .content
        - .footer

## Layout {: class="template__section" }

Here are the CSS property of all of _Ethereal_'s main layout elements.  

- html
    - display      = block
    - height       = 100%
    - box-sizing   = border-box
    - overflow-x   = hidden
- body
    - display          = flex
    - flex-direction   = column
    - position         = relative
    - box-sizing       = border-box
    - margin-bottom    = 0px
    - margin-left      = 0px
    - margin-right     = 0px
    - margin-top       = 0px
    - min-height       = 100%
    - width            = 100%
- header
    - display      = block
    - box-sizing   = border-box
    - left         = 0px
    - right        = 0px
    - top          = 0px
    - ~~position   = sticky~~
    - ~~z-index    = 4~~
- .container
    - display          = flex
    - flex-direction   = column
    - flex-grow        = 1
    - box-sizing       = border-box
- main
    - display      = block
    - flex-grow    = 1
    - box-sizing   = border-box
- .main__inner .grid
    - display          = flex
    - height           = 100%
    - margin-left      = 0px
    - margin-right     = 0px
    - margin-top       = 1.5rem
    - max-width        = 1220px
    - box-sizing       = border-box
- .sidebar .sidebar--primary
    - display          = block
    - align-self       = flex-start
    - flex-shrink      = 0
    - position         = sticky
    - height           = 100%
    - width            = 12.1rem
    - left             = -12.1rem
    - top              = 48px
    - padding-bottom   = 1.2rem
    - padding-left     = 0px
    - padding-right    = 0px
    - padding-top      = 1.2rem
    - box-sizing       = border-box
    - ~~z-index          = 5~~
- .sidebar__scrollwrap
    - display          = block
    - height           = 2239px
    - margin-bottom    = 0px
    - margin-left      = 4px
    - margin-right     = 4px
    - margin-top       = 0px
    - overflow-y       = auto
    - box-sizing       = border-box
- .sidebar__inner
    - display          = block
    - padding-right    = 4px
    - box-sizing       = border-box
- .sidebar .sidebar--secondary
    - same as .sidebar .sidebar--primary, except:
    - order = 2
- .content
    - display      = block
    - flex-grow    = 1
    - min-width    = 0px
    - box-sizing   = border-box
- .footer
    - display      = block
    - box-sizing   = border-box