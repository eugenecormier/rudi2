lilypondheader = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% LILYPOND HEADERS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\version "2.18.2"

\header {{
\ttitle = \markup {{ {font} \\fontsize #+3 {{ {title} {keytitle} }}}}
\tsubtitle = \markup {{ {font} \\fontsize #+2 Name:_______________________ }}
\ttagline = \markup {{ {font} \\fontsize #+1 {{ {tag} }}}}
\t}}

\paper {{
\t{raggedright}
\t{raggedbottom}
\t{raggedlastbottom}
\t#(set-paper-size "{papersize}"{orientation})
\t}}
\t#(set-global-staff-size {scaling})
\tindent = 0

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BAKED IN LILYPOND FUNCTIONS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
notimesig = {{ \override Staff.TimeSignature #'transparent = ##t }}
nobarline = {{ \override Staff.BarLine #'transparent = ##t }}
nobarlinenumbers = {{ \override Score.BarNumber #'transparent = ##t }}
noclef = {{ \override Staff.Clef #'transparent = ##t }}
nokeycancel = {{ \set Staff.printKeyCancellation = ##f }}
noclefresize = {{ \override Staff.Clef #'full-size-change = ##t }}
"""
