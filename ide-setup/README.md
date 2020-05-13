
## IDE Setup

### Configurations

Set the correct docstring settings

```bash
PyCharm/IntelliJ -> Preferences -> Tools -> Python Integrated Tools -> Docstring format: reStructuredText
```

### Plugins
1. RainbowBracket
2. HighlightBracketPair
3. String Manipulation
4. FileWatcher
5. AWS CloudFormation
6. cfn-lint

#### cfn-lint Plugin
MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Plugins -> Search for cfn-lint and Install it.
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> Plugins -> Search for cfn-lint and Install it.
```

#### AWS CloudFormation Plugin
MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Plugins -> Search for AWS CloudFormation and Install it.
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> Plugins -> Search for AWS CloudFormation and Install it.
```

#### FileWatcher Plugin
MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Plugins -> Search for File Watcher and Install it.
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> Plugins -> Search for File Watcher and Install it.
```

### Cloud Formation Formatting
For formatting we will use a tool called [cfn-lint](https://github.com/aws-cloudformation/cfn-python-lint). **Note: To utilize this tool you will need to move the CloudFormation portion of your serverless file to a new file. Preferably in a folder called resources. Please refer to [vtds-jenkins](https://ghe.coxautoinc.com/ETS-EDSS/vtds-jenkins) and to our [Developer Checklist](https://ghe.coxautoinc.com/ETS-EDSS/same-eng/wiki/Developer-Checklist) to see that structure.

#### cfn-lint
##### Requirements
cfn-lint requires Python >= 2.7 to be installed to work.

##### Installation
MacOS/Windows

```bash
$ pip3 install --user cfn-lint
```

##### Configuration
MacOS
```bash
$ which cfn-lint
```
Windows
```bash
$ where cfn-lint
```

Go to

MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Other Settings -> CFNLint
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Other Settings -> CFNLint
```
Select the Enable box and put the path of the `which cfn-lint` command in the exe box. Make sure to uncheck treat all issues as warnings and check Highlight whole line.


### Python Formatting
For formatting we will use a tool called [Black](https://github.com/python/black)

#### Black
##### Requirements
Black requires Python 3.6 to be installed to work.

##### Installation
MacOS/Windows

```bash
$ pip3 install --user black
```

##### Configuration
MacOS
```bash
$ which black
```
Windows
```bash
$ where black
```
if black doesn't show up, try 
```bash 
find . -type d -name "black" 2>/dev/null
```

Go to

MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Tools -> External Tools
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> External Tools
```

Click the + icon to add a new external tool with the following values:
```
Name: Black
Description: Black is the uncompromising Python code formatter.
Program: <install_location_from_which_command>
Arguments: "$FilePath$"
Uncheck Synchronize files after execution
```

##### Run Black on the Fly
MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Tools -> External Tools -> Black
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> External Tools -> Black
```

##### Run Black on Save
Go to

MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Tools -> File Watchers
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> File Watchers
```

Click + and choose '<custom>' (if asked) to add a new watcher.
```
Name: Black
File type: Python
Scope: Project Files
Program: <install_location_from_which_command>
Arguments: $FilePath$
Output paths to refresh: $FilePath$
Working directory: $ProjectFileDir$
Uncheck “Auto-save edited files to trigger the watcher”
```

### Python Linting
For linting we will use a tool called [Pylint](https://www.pylint.org/)

#### Pylint
##### Installation
MacOS/Windows
```bash
$ pip3 install --user pylint
```

##### Configuration
Download the the [same pylintrc](https://ghe.coxautoinc.com/ETS-EDSS/same-eng/blob/master/rc-files/.pylintrc) 
file. Place this file in your home directory.

MacOS
```bash
$ which pylint
```
Windows
```bash
$ where pylint
```

Go to
```bash
PyCharm/IntelliJ -> Preferences -> Tools -> External Tools
```

```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> External Tools
```

Click the + icon to add a new external tool with the following values:
```
Name: Pylint
Description: Pylint is the linting tool.
Program: <install_location_from_which_command>
Arguments: "$FilePath$"
Uncheck Synchronize files after execution
```

##### Run Pylint on the Fly
MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Tools -> External Tools -> Pylint
```

Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> External Tools -> Pylint
```

##### Run Pylint on Save
Go to

MacOS
```bash
PyCharm/IntelliJ -> Preferences -> Tools -> File Watchers
```
Windows
```bash
PyCharm/IntelliJ -> File -> Settings -> Tools -> File Watchers
```

Click + and choose '<custom>' (if asked) to add a new watcher:
```
Name: Pylint
File type: Python
Scope: Project Files
Program: <install_location_from_which_command>
Arguments: $FilePath$
Output paths to refresh: $FilePath$
Working directory: $ProjectFileDir$
Uncheck “Auto-save edited files to trigger the watcher”
```
