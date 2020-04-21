worksheetheader = """\\version "2.18.2"

\header {{
\ttitle = \markup {{ {font} \\fontsize #+3 {{ {title} }}}}
\tsubtitle = \markup {{ {font} \\fontsize #+2 Name:_______________________ }}
\ttagline = \markup {{ {font} \\fontsize #+1 {{ {tag} }}}}
"""

keysheetheader = """\\version "2.18.2"

\header {{
\ttitle = \markup {{ {font} \\fontsize #+3 {{ {title} \with-color #red Key }}}}
\tsubtitle = \markup {{ {font} \\fontsize #+2 Name:_______________________ }}
\ttagline = \markup {{ {font} \\fontsize #+1 {{ {tag} }}}}
"""