set msg=%1
git add --all
git rm --cached git.bat
git commit -m msg
git push