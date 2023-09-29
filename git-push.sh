#!/bin/bash

# Ask for the repository URL
read -p "Enter the repository URL: " repo_url

# Ask for the user's GitHub username
read -p "Enter your GitHub username: " username

# Clone the repository to the local machine
git clone $repo_url || exit 1

# Extract the repository name from the URL
repo_name=$(basename $repo_url .git)

# Change to the repository directory
cd $repo_name || exit 1

# Ask the user for a filename to create or modify
read -p "Enter a filename to create or modify: " file_name

# Create or modify the file
echo "This is the first commit." > $file_name

# Add all changes to staging
git add .

# Commit the changes
git commit -m "First commit."

# Set up remote with authentication
git remote set-url origin https://$username:@$repo_url

# Push the changes to GitHub
git push origin master || exit 1

echo "First commit successful!"
