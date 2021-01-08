header = """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Identify/Write Notes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\markup {{ {boldfont} {{ Identifying and Writing Notes }}}}
"""

identText = """\markup {{ {font} {{ Identify the following notes. }}}}
"""
identSectionStart = """{{ \override TextScript.staff-padding = #6 \\notimesig \\nobarline \clef {clef} """

identLoop = """{note}_\markup \center-align {{ {key} }} """

identSectionEnd = """}"""



writeText = """\markup {{ {font} {{ Write the following notes. }}}}
"""
writeSectionStart = """{{ \clef {clef} """
writeSectionEnd = """}}"""


# notes and keys for each clef
trebleNotes = ["d'", "e'", "f'", "g'", "a'", "b'", "c''", "d''", "e''", "f''", "g''"]
trebleKey = ['SD', 'LE', 'SF', 'LG', 'SA', 'LB', 'SC', 'LD', 'SE', 'LF', 'SG']

tenorNotes = ["c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'"]
tenorKey = ['SC', 'LD', 'SE', 'LF', 'SG', 'LA', 'SB', 'LC', 'SD', 'LE', 'SF']

altoNotes = ["e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'"]
altoKey = ['SE', 'LF', 'SG', 'LA', 'SB', 'LC', 'SD', 'LE', 'SF', 'LG', 'SA']

bassNotes = ["f,", "g,", "a,", "b,", "c", "d", "e", "f", "g", "a", "b"]
bassKey = ['SF', 'LG', 'SA', 'LB', 'SC', 'LD', 'SE', 'LF', 'SG', 'LA', 'SB']

trebleLedgerNotes = ["f", "g", "a", "b", "c'", "a''", "b''", "c'''", "d'''", "e'''"]
trebleLedgerKey = ['LF', 'SG', 'LA', 'SB', 'LC', 'LA', 'SB', 'LC', 'SD', 'LE']

tenorLedgerNotes = ["e,", "f,", "g,", "a,", "b,", "g'", "a'", "b'", "c''", "d''"]
tenorLedgerKey = ['LE', 'SF', 'LG', 'SA', 'LB', 'LG', 'SA', 'LB', 'SC', 'LD']

altoLedgerNotes = ["g,", "a,", "b,", "c", "d", "b'", "c''", "d''", "e''", "f''"]
altoLedgerKey = ['LG', 'SA', 'LB', 'SC', 'LD', 'LB', 'SC', 'LD', 'SE', 'LF']

bassLedgerNotes = ["a,,", "b,,", "c,", "d,", "e,", "c'", "d'", "e'", "f'", "g'"]
bassLedgerKey = ['LA', 'SB', 'LC', 'SD', 'LE', 'LC', 'SD', 'LE', 'SF', 'LG']
