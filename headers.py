lilypondheader = """\\version "2.18.2"

\header {{
\ttitle = \markup {{ {font} \\fontsize #+3 {{ {title} {keytitle} }}}}
\tsubtitle = \markup {{ {font} \\fontsize #+2 Name:_______________________ }}
\ttagline = \markup {{ {font} \\fontsize #+1 {{ {tag} }}}}
\t}}

\paper {{
\tragged-right = ##f
\tragged-bottom = ##f
\tragged-last-bottom = ##f

"""
