# Contributing to GoodMorningTech 💻📝

Thank you for your interest in contributing to GoodMorningTech! 🙌 Whether you're a programmer 💻, writer 📝, or community helper 🤝, your contributions are greatly appreciated. 

## Table of Contents 
1. [How to Contribute](#how-to-contribute)
2. [Code of Conduct](#code-of-conduct)
3. [Getting Started](#getting-started)
4. [Bug Reporting](#bug-reporting)
5. [Enhancement Requests](#enhancement-requests)
6. [Contact Information](#contact-information)

## How to Contribute 🤔

Here are a few ways you can contribute to the GoodMorningTech project: 

- **Programming**: If you have programming experience and would like to contribute to the code base, check out the [open issues](https://github.com/GoodMorninTech/GoodMorningTech/issues) to see what needs to be done or create an issue or pull request, and we will review it. Before you start working on a new feature or bug fix, make sure to fork the project and work on the development branch and open a pull request when you're ready to submit your changes. 💻

- **Writing**: If you have a passion for writing and would like to contribute to our news, Apply at this link [Application Link](https://goodmorningtech.news/writers/apply), if we accept you we will reach out. 📝

- **Community Help**: If you'd like to help out the community in any way, let us know, or join our [discord](https://discord.goodmorningtech.news)! We're always looking for ways to improve and make a positive impact. 🤝

## Code of Conduct 📜

To ensure that the GoodMorningTech community is welcoming and inclusive to all, we have a [Code of Conduct](CODE_OF_CONDUCT.md) that all contributors must follow. Please take a moment to read it before contributing. 

## Getting Started 🚀

To get started fork the Repository on GitHub.

### Prerequisites
- Python
- Node.js

If you don't have these just install them from the official websites.

#### Cloning the repository
Clone the forked repository(make sure to insert your username):
```
git clone https://github.com/YOURGITHUBUSERNAME/GoodMorningTech.git
```
Move into the new directory:
```
cd GoodMorningTech
```
#### Configuration
Create an `instance` folder:
```
mkdir instance
```
Move the configuration template into `instance` and rename it to `config.py`:
Windows:
```
copy config.template.py config.py
move config.py instance
```
Linux:
``` 
cp config.template.py config.py
mv config.py instance
```
Edit the configuration file and set the fields to your liking.

For the database to work create a mongoDB database and set the `MONGO_URI` to your database.

To use the email functionality set the `MAIL_USERNAME`,`MAIL_PASSWORD` and `MAIL_SERVER`
to your email credentials, for gmail you might need to configure extra stuff,
look up recent guides on how to use SMTP with gmail.

Alternatively you can configure everything from environment variables, make sure to set all the variables in `config.template.py`.

#### Set Up for Development
Install the development requirements:
```
pip install -r requirements-dev.txt
```
```
npm install
```

[//]: # (#### Install pre-commit hooks:)

[//]: # (```)

[//]: # (pre-commit install)

[//]: # (```)

#### Running the Server
Install the requirements:
```
pip install -r requirements.txt
```
Run the application:
```
python -m flask --app gmt --debug run 
```
and in separate terminal run the tailwind compiler:
```
npm run tailwind
```

## Bug Reporting 🐛

If you find a bug in the project, we would love to know about it! Before reporting a bug, please check the [open issues](https://github.com/GoodMorninTech/GoodMorningTech/issues) to see if it has already been reported. If not, please create a new issue and provide as much detail as possible about the bug, including steps to reproduce it. 

## Enhancement Requests 💡

If you have an idea for a new feature or enhancement, we'd love to hear about it! Before creating a new enhancement request, please check the [open issues](https://github.com/GoodMorninTech/GoodMorningTech/issues) to see if it has already been suggested. If not, please create a new issue and provide as much detail as possible about the enhancement. 

## Contact Information 📞

If you have any questions or would like to get in touch with us, feel free to send us an email at [support@goodmorningtech.news](mailto:support@goodmorningtech.news) or join our Discord server at [discord.goodmorningtech.news](https://discord.goodmorningtech.news/). We're always here to help and support you in your contributions! 🤗
