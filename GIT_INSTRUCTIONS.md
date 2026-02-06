# Git Instructions for Section 1.3

This document contains the Git commands required by Section 1.3 of the assignment.

## Scenario

Your successfully created project is on the Version Control System Git and has a branch called `develop`. On this branch, all operations of the developer team are combined.

## Task 1: Clone the Branch and Develop on Your Local PC

To clone the repository and work on the `develop` branch locally:

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd <project-directory>

# Checkout the develop branch (if not already on it)
git checkout develop

# Pull the latest changes from the remote develop branch
git pull origin develop
```

If you want to create a local tracking branch for develop:

```bash
# Fetch all branches from remote
git fetch origin

# Checkout and track the remote develop branch
git checkout -b develop origin/develop
```

## Task 2: Adding a New Function and Introducing It to the Team's Develop Branch

After you have added a new function to your code, follow these steps:

### Step 1: Stage Your Changes

```bash
# Check the status of your changes
git status

# Stage specific files (if you want to be selective)
git add <file1> <file2>

# OR stage all changes
git add .
```

### Step 2: Commit Your Changes

```bash
# Commit your changes with a descriptive message
git commit -m "Add new function: description of what the function does"
```

Example commit message:
```bash
git commit -m "Add function to calculate additional statistics for test data mapping"
```

### Step 3: Push Your Changes to Your Remote Branch

```bash
# Push your local develop branch to your remote branch (fork)
git push origin develop
```

If this is your first push or if the branch doesn't exist remotely yet:

```bash
# Push and set upstream tracking
git push -u origin develop
```

### Step 4: Create a Pull Request

After pushing, you need to create a Pull Request (PR) to merge your changes into the team's `develop` branch:

1. **Via GitHub/GitLab Web Interface:**
   - Go to your repository on GitHub/GitLab
   - Click on "Pull Requests" or "Merge Requests"
   - Click "New Pull Request" or "New Merge Request"
   - Select `develop` as the base branch (where you want to merge into)
   - Select your branch (also `develop` in this case, or your feature branch)
   - Add a descriptive title and description
   - Click "Create Pull Request" or "Create Merge Request"

2. **Via Command Line (GitHub CLI - if installed):**
   ```bash
   gh pr create --base develop --head develop --title "Add new function" --body "Description of changes"
   ```

### Step 5: Review and Merge

After creating the Pull Request:

1. Team members will review your code
2. Address any feedback or requested changes
3. If changes are requested:
   ```bash
   # Make the changes
   # Stage and commit again
   git add .
   git commit -m "Address review feedback: description of changes"
   git push origin develop
   ```
   The PR will automatically update with your new commits

4. Once approved, a team member (usually a maintainer) will merge your Pull Request into the `develop` branch

5. After merging, update your local `develop` branch:
   ```bash
   # Fetch the latest changes from remote
   git fetch origin
   
   # Merge the updated develop branch into your local branch
   git pull origin develop
   ```

## Complete Workflow Summary

Here's the complete workflow in one sequence:

```bash
# 1. Clone the repository and checkout develop
git clone <repository-url>
cd <project-directory>
git checkout develop
git pull origin develop

# 2. Make your changes (edit files, add new function, etc.)

# 3. Stage your changes
git add .

# 4. Commit your changes
git commit -m "Add new function: description"

# 5. Push to remote
git push origin develop

# 6. Create Pull Request via web interface (see instructions above)

# 7. After PR is merged, update your local branch
git pull origin develop
```

## Additional Useful Commands

```bash
# View commit history
git log

# View differences in your working directory
git diff

# View differences for staged changes
git diff --staged

# Create a new branch for a feature (if working on a feature branch)
git checkout -b feature/new-function
# ... make changes ...
# When ready, merge feature branch into develop
git checkout develop
git merge feature/new-function
```

## Notes

- Always pull the latest changes before starting work: `git pull origin develop`
- Write clear, descriptive commit messages
- Keep commits focused and logical
- Test your code before committing
- Communicate with your team about major changes
- Follow your team's code review process

