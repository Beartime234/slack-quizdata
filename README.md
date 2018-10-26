# Slack Quiz Data

This repository holds questions for the following slack quizzes

- [pokequiz](https://pokequiz.xyz)

## Getting Started

If you would like to submit your own question or make changes to the current
questions you can find them under the [questions](https://github.com/Beartime234/slack-quizdata/tree/master/questions) directory.
For more instructions on how to submit your own questions view [SUBMITTING_QUESTIONS](docs/SUBMITTING_QUESTIONS.md).

The project has two main parts to it. The 'uploader' which is python code responsible
for uploading and validating the questions to the database when you push to master.
As well as the quiz questions which are YAML based files which store quiz question
information for a range of quizzes.

### Prerequisites

The 'uploader' runs on Python 3.6+ so make sure you have that installed.
You will also need [pipenv](https://pipenv.readthedocs.io/en/latest/) installed.

You can install pipenv using brew

```
brew install pipenv
```

### Installing

This project uses [pipenv](https://pipenv.readthedocs.io/en/latest/) for
dependency management.

To install the required packages run the following command

```
pipenv sync --dev
```

### Adding a question

There is a simple command line based prompt tool which can help you
add questions easily. You can run this with the following command

```
pipenv run python -m uploader.create
```

this will help you add questions to the yaml files located under questions/
before submitting these questions double check the questions you have updated
to make sure the questions were added correctly.

There are detailed examples on how to do this under [SUBMTTING_QUESTIONS](docs/SUBMITTING_QUESTIONS.md)

## Running The Tests

### Question Validator

To run the question validator to make sure your questions are valid before
submitting them run the following command from the root directory.

```
pipenv run python -m uploader.validate
```

This will check that your questions are valid and follow question guidelines.

TODO add question guidelines doc

### Uploader Tests

To run the unit tests on the uploader code run the following from
the root directory.

```
pipenv run python -m pytest tests/ -vv
```

## Deployment

You need to have two environment variables set before deploying the questions. As
it is built for CICD pipelines and shouldn't really be used directly.

AWS_PROFILE: Your local AWS profile which gives you access to the quiz data
storage table.

QUIZ_STORAGE_TABLE: The name of the table that you will be uploading the questions
too. For information on how to set this up see Database.

To deploy the code into the database you would run the following command
from the root directory. Make sure you have validated the questions before
uploading them.

```
pipenv run python -m uploader.update
```

### Database

but this will not work unless you have a database. You can
run your own version of the database by building [templates/data.yml](templates/data.yml)
If your pull request has been approved and merged to master this code will run
to move the questions into the quiz question table. So you shouldn't have
to worry about it unless there is an issue with it.

## Built With

* [Slack API](http://www.api.slack.com)
* [Python Slack Client](https://slackapi.github.io/python-slackclient/)
* [YAML](http://yaml.org)
* [Prompt Toolkit](https://github.com/jonathanslenders/python-prompt-toolkit)

## Contributing

Please read [CONTRIBUTING](docs/CONTRIBUTING.md)
for details on how to raise issues and the process for submitting pull requests.

For submitting a question see [SUBMITTING_QUESTIONS](SUBMITTING_QUESTIONS.md).

## Authors

* **Joshua Eaton** - *Owner* - [Beartime234](https://github.com/beartime234)

