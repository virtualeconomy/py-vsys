# Developing Documentation

- [Developing Documentation](#developing-documentation)
  - [Philosophy](#philosophy)
  - [Workflow](#workflow)
  - [Set Up Development Environment](#set-up-development-environment)
  - [Code Style Guide](#code-style-guide)
  - [Git Commit Style](#git-commit-style)
    - [Commit Format](#commit-format)
  - [Branch & PR Naming Convention](#branch--pr-naming-convention)
  - [Github Issue Naming Convention](#github-issue-naming-convention)
  - [Doc String Guide](#doc-string-guide)

## Philosophy

>***Code Quality Matters! User Experience Matters!***

>***Code Quality Matters! User Experience Matters!***

>***Code Quality Matters! User Experience Matters!***


- ***Keep it Simple, Stupid, Clear, & Clean***.

- ***No Over-Engineering***. Don't do things for the sake of doing things. Every technical decision has to be made for specific reasons and leads to gains(e.g. improves readability, maintainability user experience, etc).

- ***Premature Optimization is the Root of All Evil***. Good enough is perfect. Let it grow first and optimize it later on if necessary.

- ***Iterative Mindset***. Don't try to do everything in one go. Keep every change small & clear.


## Workflow

[Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow) is used.
To contribute, please work on a forked repo and create a PR from the forked repo to the `develop` branch of the main repo.

The main repo will have 3 branches:
- **main**: The latest version that is released.
- **develop**: The latest version that is being worked on. **The default branch**.
- **release**: The version that is going to be released. The **release** branch shall be checked out from the **develop** branch and be tested. All fixes shall be committed to the **release** branch directly. When the test passed, the **release** branch shall be merged into the **main** branch with a tag of the released version and be merged to the **develop** branch as well if there is any fixes commits.


## Set Up Development Environment
The development requires `Python 3.9`. Dependencies for development will be managed by [Pipenv](https://github.com/pypa/pipenv).

To set up the development environment, go to the project root directory and

1. Install dependencies with [Pipenv](https://github.com/pypa/pipenv) and use [Pipenv](https://github.com/pypa/pipenv) shell as the shell environment.

    ```bash
    pipenv install -d
    pipenv shell
    ```

2. Install Git hooks with [pre-commit](https://github.com/pre-commit/pre-commit) in the Pipenv shell so that the Python formatter [black](https://github.com/psf/black) will be triggered for each commit.

    ```bash
    pre-commit install
    ```


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

## Github Issue Naming Convention

The naming convention for Github issues conforms to the PR one.

```
type: short summary in lower case
  │               │
  │               └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|docs|feat|fix|refactor|test|chore 
```

For example, to suggest adding test cases, the issue name should look like

```
test: add test cases for XXX
```

To file a bug, the issue name should look like

```
fix: XXX is incorrect
```


## Doc String Guide

Doc string is a must for wherever it is applicable (e.g. module, class, function, method, etc) so that API references documentation can be auto-generated out of it.

`py-v-sdk` follows [Google Style](https://stackoverflow.com/a/24385103) and borrows from Golang the idea of starting the commentary always with the name of the object you'd like to comment.

Below is an example.

```python
@abstractmethod
def issue(self, by: acnt.Account, description: str = "") -> Dict[str, Any]:
    """
    issue issues a token.

    Args:
        by (acnt.Account): The action taker.
        description (str): The description of this action. Defaults to "".

    Returns:
        Dict[str, Any]: The response returned by the Node API.

    Raises:
        NotImplementedError: Left to be implemented by the sub class.
    """
    raise NotImplementedError
```
For folks using VSCode, the plugin [Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) is recommended to quickly generate the doc string template.
