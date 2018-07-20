#### Renaming Branches for both local and remote

1. Rename your local branch. <br>
   If you are on the branch you want to rename:
```
git branch -m new-name
```
   If you are on a different branch:<br>
```
git branch -m old-name new-name
```
2. Delete the old-name remote branch and push the new-name local branch.
```
git push origin :old-name new-name
```
3. Reset the upstream branch for the new-name local branch.<br>
  Switch to the branch and then:
```
git push origin -u new-name
```
