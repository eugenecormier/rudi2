header = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Draw Clefs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\markup {{ {boldfont} {{ Drawing Clefs }}}}
"""

clefone = """{{ \\nobarline \\notimesig \\noclefresize 
  \clef {clef}  s4
  {forceclef} \override Staff.Clef #'color = #(rgb-color 1.0 0.0 0.0) \clef {clef}  s4
  {forceclef} \clef {clef}  s4
  {forceclef} \clef {clef}  s4 \\noBreak
  {forceclef} \clef {clef}  \stopStaff s4 

"""

cleftwo = """{startstaff} {forceclef} \\revert Staff.Clef #'color \clef {clef} s4
  {forceclef} \override Staff.Clef #'color = #(rgb-color 1.0 0.0 0.0) \clef {clef} s4
  {forceclef} \clef {clef} s4 \\noBreak
  {forceclef} \clef {clef} s4
  {forceclef} \clef {clef} }}

"""