# Good Morning Tech
Get a daily dose of tech news in your mailbox! Good Morning Tech is a daily newsletter that delivers the most important tech news of the day. It's a great way to stay up to date with the latest tech news without having to spend hours on the internet.
It's 100% automated and it's free! You can even set your time zone so that you get the news at the right time.

## Work in progress
This project is still a work in progress. It's not ready for production yet. If you want to help, feel free to make a pull request!
## How does it work?
It gets the important posts from the Verge tech news section and sends them to your email address.

### How do I subscribe?
You can subscribe to Good Morning Tech by clicking [here](https://goodmorningtech.simonrijntjes.nl/register).
### How do I unsubscribe?
You can unsubscribe from the link in the footer of the newsletter.

## Getting Started
Clone the repository:
```
git clone https://github.com/GoodMorninTech/GoodMorningTech.git
```
Move into the new directory:
```
cd GoodMorningTech
```
### Configuration
Create an `instance` folder:
```
mkdir instance
```
Move the configuration template into `instance` and rename it to `config.py`:
```
mv config.py.template instance/config.py
```
Edit the configuration file and make sure to set the following fields:
- `SECRET_KEY`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`

Alternatively you can oonfigure everything from environment variables, make sure to set all the variables in `config.py.template`, but prefix them with `FLASK_`.
### Running the Server
Install the requirements:
```
pip install -r requirements.txt
```
Run the application:
```
python index.py
```
### Set Up for Development
Install the development requirements:
```
pip install -r requirements-dev.txt
```
Install pre-commit hooks:
```
pre-commit install
```
