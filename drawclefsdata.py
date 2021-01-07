header = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Draw Clefs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\markup {{ {boldfont} {{ Drawing Clefs }}}}
\markup {{ {font} {{ Draw the following clef(s) {number} times. }}}}
"""

clefone = """{{ \\nobarline \\notimesig \\noclefresize 
  \clef {clef}  s4
  {key} \set Staff.forceClef = ##t \override Staff.Clef #'color = #(rgb-color 1.0 0.0 0.0) \clef {clef}  s4
  {key} \set Staff.forceClef = ##t \clef {clef}  s4
  {key} \set Staff.forceClef = ##t \clef {clef}  s4 \\noBreak
  {key} \set Staff.forceClef = ##t \clef {clef}  \stopStaff s4 

"""

cleftwo = """{startstaff} \set Staff.forceClef = ##t \\revert Staff.Clef #'color {hideclef}\clef {clef} s4
  {key} \set Staff.forceClef = ##t \override Staff.Clef #'color = #(rgb-color 1.0 0.0 0.0) \clef {clef} s4
  {key} \set Staff.forceClef = ##t \clef {clef} s4 \\noBreak
  {key} \set Staff.forceClef = ##t \clef {clef} s4
  {key} \set Staff.forceClef = ##t \clef {clef} }}

"""
