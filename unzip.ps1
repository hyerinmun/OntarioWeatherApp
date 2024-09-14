$backup= 7z e C:\CollaborativeProject\SCRIBE.NWCSTG.05.08.14Z.n.Z  -oC:\CollaborativeProject\output 
$backup
Rename-Item -Path "C:\CollaborativeProject\output\SCRIBE.NWCSTG.05.08.14Z.n" -NewName "SCRIBE.NWCSTG.05.08.14Z.txt"
