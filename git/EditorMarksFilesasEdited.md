#### My editor marks my files as edited when I open them!

This is the intended behavior of the EditorConfig VS Code plugin when end_of_line is set to lf (as it is in CX) and the file is opened in a Windows OS. To fix this behavior in an existing Git repository, run the following commands (warning: this will discard all current changes and revert to the last commit):
```
git config core.autocrlf false 
git rm --cached -r . 
git reset --hard
```
The above commands prevent Git from converting the line endings to the Windows CR/LF on checkout so that EditorConfig's expectation of Unix line endings is met. More info here.
