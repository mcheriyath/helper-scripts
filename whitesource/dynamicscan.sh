#!/bin/bash

# Check https://whitesource.atlassian.net/wiki/spaces/WD/pages/33718339/File+System+Agent 
# for latest version of filesystem agent
WSAGENT="whitesource-fs-agent-1.8.7.jar"
WSCONFIG="whitesource.config"
WSTOKEN="projecttoken"
HOME_DIR=$HOME
BUILDTOOL_PATH=/path/to/buildtool
STASH_URL="https://Mithun.Cheriyath@stash.example.com/project/repo"
REF=$1
BUILD_NUMBER=$(echo $REF|cut -f2 -d/)
REPO_DIR=$HOME/repos
PLATFORM=$2

# Create the repos dir if its not created yet
if [ -d "$REPO_DIR" ]; then
    echo "Using the existing $REPO_DIR"
else
    echo "Creating $REPO_DIR."
    mkdir $REPO_DIR
fi

# Checking the availability of whitesource filesystem agent
if [ -f "$REPO_DIR/$WSAGENT" ]
then
	echo "$WSAGENT found."
else
	echo "$WSAGENT not found."
	echo "Downloading from Whitesource Website"
	curl -o $REPO_DIR/$WSAGENT https://s3.amazonaws.com/file-system-agent/$WSAGENT
fi

function gitclone {
    cd $REPO_DIR
    REPO_URL="$STASH_URL/$1.git"
    echo "Cloning $REPO_URL"
    if [ ! -d "$1" ]; then
        git clone $REPO_URL
    fi
}

function updategit {
    cd $REPO_DIR/$1
    git fetch origin
    git pull origin
}

function switchversion {
    gitclone $1
    updategit $1
    git checkout $2
}

function generate_extsrc_references {
	echo "Building Thirdparty Component log on $REPO_DIR/BUILD_$BUILD_NUMBER.log"
	$BUILDTOOL_PATH --plat $1 THIRDPARTYCOMP > $REPO_DIR/BUILD_$BUILD_NUMBER.log
	if [ $? -eq 0 ]; then
	    echo "Generating tpip extsrc paths on $REPO_DIR/EXTSRC_$BUILD_NUMBER.out"
		grep Thirdparty $REPO_DIR/BUILD_$BUILD_NUMBER.log > $REPO_DIR/THIRDPARTYCOMP_$BUILD_NUMBER.out
		grep -oP '\K/extsrc.*,' $REPO_DIR/THIRDPARTYCOMP_$BUILD_NUMBER.out | grep -oP '.*(?=,$)' > $REPO_DIR/EXTSRC_$BUILD_NUMBER.out
	else
    	echo "NBBUILDTOOL failed to generate the required output.."
		exit
	fi
}

function check_if_path_exists {
	FILEPATHS=$(cat $REPO_DIR/EXTSRC_$BUILD_NUMBER.out)
	echo "Checking if file or folder path mentioned in $REPO_DIR/EXTSRC_$BUILD_NUMBER.out exists."
	for path in $FILEPATHS
    do
        #echo "checking if folder or path : $path exists.."
        if [ -f "$path" ]; then
                #echo "file $path exists..."
                echo "$path" >> $REPO_DIR/EXTSRC_PATHEXISTS_$BUILD_NUMBER.txt
        elif [ -d "$path" ]; then
                #echo "folder $path exists..."
                echo "$path" >> $REPO_DIR/EXTSRC_PATHEXISTS_$BUILD_NUMBER.txt
        else
                echo "$path" >> $REPO_DIR/EXTSRC_NOTFOUND_$BUILD_NUMBER.path
        fi
	done
	echo "Sorting files and folders not found onto $REPO_DIR/EXTSRC_NOTFOUND_$BUILD_NUMBER.path"
	echo ""
	echo "Sorting found files and folders onto $REPO_DIR/EXTSRC_PATHEXISTS_$BUILD_NUMBER.txt"
}

function sort_uniq_path {
	echo "Building list of file/folder paths to be scanned by whitesource fs agent."
	if [ -f $REPO_DIR/EXTSRC_PATHEXISTS_$BUILD_NUMBER.txt  ]; then
		cat $REPO_DIR/EXTSRC_PATHEXISTS_$BUILD_NUMBER.txt | sort | uniq > $REPO_DIR/SORTED_EXTSRC_$BUILD_NUMBER.txt
	else
		echo "File not found. Existing the script"
		exit
	fi
	echo "Removing unwanted references.."
	UNWANTED_EXTSRC_REF=$(grep -vE '[0-9]' $REPO_DIR/SORTED_EXTSRC_$BUILD_NUMBER.txt)
	echo "Building extsrc references with the versions.."
	grep -E '[0-9]' $REPO_DIR/SORTED_EXTSRC_$BUILD_NUMBER.txt > $REPO_DIR/EXTSRC_$BUILD_NUMBER.path
	for uwpath in $UNWANTED_EXTSRC_REF
	do
		if [ -f "$uwpath" ]; then
			echo $uwpath >> $REPO_DIR/EXTSRC_$BUILD_NUMBER.path
		else
			echo "Removing $uwpath from the final list."
		fi
	done
	echo "Completed sorting files/folders to scan...."
	echo "Whitesource fs agent input written to $REPO_DIR/EXTSRC_$BUILD_NUMBER.path"
}

switchversion src $REF
generate_extsrc_references $PLATFORM
check_if_path_exists
sort_uniq_path


# Creating the Whitesource Configuration file
if [ -f "$REPO_DIR/$WSCONFIG" ]
then
	echo "Using the already existing whitesource.config."
else
	echo "Creating whitesource.config from template"
cat << EOF > $REPO_DIR/$WSCONFIG
apiKey=$WSTOKEN
productToken=
projectToken=
includes=**/*.c **/*.cc **/*.cp **/*.cpp **/*.cxx **/*.c++ **/*.h **/*.hpp **/*.hxx **/*.dll **/*.cs **/*.c# **/*.csharp **/*.jar **/*.so
excludes=**/*sources.jar **/*javadoc.jar
case.sensitive.glob=false
followSymbolicLink=true
npm.resolveDependencies=false
bower.resolveDependencies=false
nuget.resolveDependencies=false
archiveExtractionDepth=5
archiveIncludes=**/*.war **/*.tar **/*.ear **/*.gz **/*.tar.gz **/*.1.gz **/*.tgz **/*.tar.bz2 **/*.zip
#archiveExcludes=**/*sources.jar
EOF
fi

echo "Running whitesource filesystem agent on file $REPO_DIR/EXTSRC_$BUILD_NUMBER.path"
time java -jar $REPO_DIR/$WSAGENT -c $REPO_DIR/$WSCONFIG -f $REPO_DIR/EXTSRC_$BUILD_NUMBER.path -product $BUILD_NUMBER  -project $PLATFORM > $REPO_DIR/WHITESOURCE-SCAN-$BUILD_NUMBER.log
