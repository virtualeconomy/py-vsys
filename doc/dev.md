# Developing Documentation

## Workflow

[Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow) is used.
To contribute, please work on a forked repo and create a PR from the forked repo to the `develop` branch of the main repo.

The main repo will have 3 branches:
- **main**: The latest version that is released.
- **develop**: The latest version that is being worked on. **The default branch**.
- **release**: The version that is going to be released. The **release** branch shall be checked out from the **develop** branch and be tested. All fixes shall be committed to the **release** branch directly. When the test passed, the **release** branch shall be merged into the **main** branch with a tag of the released version and be merged to the **develop** branch as well if there is any fixes commits.


## Code Style Guide

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) is adopted.


## Git Commit Style

`py-v-sdk`'s commit style is a **simplified** version of [Angular Commit style](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format).

### Commit Format
```
<type>: <short summary>
  │               │
  │               └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|docs|feat|fix|refactor|test|chore
```

Commit Type must be one of the following:

- **build**: Changes that relate to dependencies, CI, etc
- **docs**: Documentation only changes
- **feat**: A new feature
- **fix**: A bug fix
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **test**: Adding missing tests or correcting existing tests
- **chore**: Other trivial changes

## Branch & PR Naming Convention

A branch and the PR comes from it should be small(i.e. contains small-scale changes for only 1 aspect). 

The naming convention for branch
```
type/short-summary-in-lower-case
  │               │
  │               └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|docs|feat|fix|refactor|test|chore
```

The naming convention for PR
```
type: short summary in lower case
  │               │
  │               └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|docs|feat|fix|refactor|test|chore 
```

For example, say we would like to add the branch naming convention to the documentation.
The branch name should look like
```
docs/add-branch-naming-convention
```

The PR should look like

```
docs: add branch naming convention
```