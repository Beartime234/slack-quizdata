# Slack Quiz Data


This repository holds questions for the following slack quizzes

- [pokequiz](https://pokequiz.xyz)

## Getting Started

If you would like to submit your own question or make changes to the current
questions you can find them under the [questions](https://github.com/Beartime234/slack-quizdata/tree/master/questions) directory.
For more instructions on how to submit your own questions view docs.

The project has two main parts to it. The 'uploader' which is python code responsible
for uploading and validating the questions to the database when you push to master.
As well as the quiz questions which are YAML based files which store quiz question
information for a range of quizzes.

### Prerequisites

The 'uploader' runs on Python 3+ so make sure you have that installed.
You will also need [pipenv](https://pipenv.readthedocs.io/en/latest/) installed.

You can install pipenv using brew

```
brew install pipenv
```

### Installing

This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/) for dependency management.

To install the required packages run the following command

```
pipenv sync --dev
```

## Running The Tests

### Question Validator

To run the question validator to make sure your questions are valid before
submitting them run the following command from the root directory.

```
pipenv run python -m uploader.question_validator
```

### Uploader Tests

To run the unit tests on the uploader code run the following from
the root directory.

```
pipenv run python -m pytest tests/ -vv
```

## Deployment

To deploy the code into the database you would run the following command
from the root directory.

```
pipenv run python -m uploader.question_updater
```

but this will not work unless you have set up your own database. If your
pull request has been approved and merged to master this code will run
to move the questions into the quiz question table. So you shouldn't have
to worry about it unless there is an issue with it.

## Built With

* [Slack API](http://www.api.slack.com)
* [Python Slack Client](https://slackapi.github.io/python-slackclient/)
* [YAML](http://yaml.org)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426)
for details on how to add questions, change the updating code and the
process for submitting pull requests.

## Authors

* **Joshua Eaton** - *Initial work and owner* - [Beartime234](https://github.com/beartime234)

