#!/bin/sh
set -e -x

# Verify our environment variables are set
[ -z "${GIT_REPO}" ] && { echo "Need to set GIT_REPO"; exit 1; }
[ -z "${GIT_BRANCH}" ] && { echo "Need to set GIT_BRANCH"; exit 1; }
[ -z "${GIT_ORIGIN}" ] && { echo "Need to set GIT_ORIGIN"; exit 1; }
[ -z "${COMMIT_USER}" ] && { echo "Need to set COMMIT_USER"; exit 1; }
[ -z "${COMMIT_EMAIL}" ] && { echo "Need to set COMMIT_EMAIL"; exit 1; }
[ -z "${WORKING_DIR}" ] && { echo "Need to set WORKING_DIR"; exit 1; }
[ -z "${SSH_KEY}" ] && { echo "Need to set SSH_KEY"; exit 1; }
[ -z "${FILES_TO_COMMIT}" ] && { echo "Need to set FILES_TO_COMMIT"; exit 1; }

# Change to our working directory
cd ${WORKING_DIR}

# Set up our SSH Key
if [ ! -d ~/.ssh ]; then
	echo "SSH Key was not found. Configuring SSH Key."
	mkdir ~/.ssh
	cp "${SSH_KEY}" ~/.ssh/id_rsa
	chmod 700 ~/.ssh
	chmod 600 ~/.ssh/id_rsa

	echo -e "Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile=/dev/null\n" > ~/.ssh/config
fi

# Check to see if the given directory already has an initialized
# git repository.
if [ ! -d "${WORKING_DIR}/.git" ]; then
	echo "Git repository not found. Initializing repository."
	git init 
	git remote add ${GIT_ORIGIN} ${GIT_REPO}
	git fetch
	git checkout -t ${GIT_ORIGIN}/${GIT_BRANCH}
fi

# Configure our user and email to commit as.
git config --global user.name "${COMMIT_USER}"
git config --global user.email "${COMMIT_EMAIL}"



# Check to see if there are changes
CHANGES=`git status -s | awk {'print $2'}`
if [ -z "${CHANGES}" ]; then
	echo "No changes detected."
	continue
fi

# Check to see if we need to commit all.
git add "data.json" "bot_scores.md" 
CHANGES_FOUND="1"
git status

# Commit and push the detected changes if they are found.
if [ ! -z "${CHANGES_FOUND}" ]; then
	echo "Changes detected."
	git commit -m "Auto Build Scoreboard."
	git push ${GIT_ORIGIN} ${GIT_BRANCH}
fi
