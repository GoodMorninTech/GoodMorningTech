# Good Morning Tech
<div align="center">
<img width=20% src="https://user-images.githubusercontent.com/65854503/213913237-e8ceeb02-68f9-4b78-80f7-c249f7a29f22.png">
<br>
<h3>We are an open-source tech newsletter, sign up and stay updated with the latest news in tech at your convenience! Oh did I mention, we are 100% free?</h3>
<a href="https://goodmorningtech.news/">Checkout our website</a> • <a href="https://goodmorningtech.news/">Get in touch with us</a> • <a href="https://example.com">Report a bug</a>
</div>
<div align="center">

<br>

![Project Details](https://img.shields.io/github/repo-size/goodmornintech/goodmorningtech?color=red&label=Project%20Size&style=for-the-badge)
![License](https://img.shields.io/github/license/goodmornintech/goodmorningtech?color=red&style=for-the-badge)
![Stars](https://img.shields.io/github/stars/goodmornintech/goodmorningtech?color=red&label=Project%20Stars&style=for-the-badge)
![Contributors](https://img.shields.io/github/contributors/goodmornintech/goodmorningtech?color=red&style=for-the-badge)
</div>
<div>
  </div>
<br>

<div align="left"></div>

<details align="left">
  <summary>Table of Content:</summary>
  <ol>
    <li>
      <a href="#learn-more-about-this-project">Learn more about this project</a>
      <ul>
        <li><a href="#screenshots">Screenshots</a></li>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#get-started">Get started</a>
      <ul>
        <li><a href="#contribute">Contribute</a></li>
        <li><a href="#setting-up-on-your-local-machine">Setting up on your local machine</a></li>
      </ul>
    </li>
    <li><a href="#whats-planned-ahead">What's planned ahead</a></li>
    <li><a href="#frequently-asked-questions-faqs">Frequently Asked Question's (FAQs)</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact-us">Contact Us</a></li>
    <li><a href="#authors">Authors</a></li>
  </ol>
</details>
</div>

## Learn more about this project

![image](https://user-images.githubusercontent.com/62475932/213938986-6a1fe609-8ef9-4dcf-93b0-720ce5739e2d.png)


### Built With
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![Adobe Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white)
![Dribbble](https://img.shields.io/badge/Dribbble-EA4C89?style=for-the-badge&logo=dribbble&logoColor=white)
<br>
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
<br>
![NPM](https://img.shields.io/badge/NPM-%23000000.svg?style=for-the-badge&logo=npm&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
<br>
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Vercel](https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white)
![Cybrancee](https://custom-icon-badges.demolab.com/badge/Cybrancee-ebeff0?style=for-the-badge&logo=cybrancee&logoColor=pink)
<br>


### Features

- Timezone Selection
- Time Selection
- Days Selection
- Article Count Selection

## Get started
### Contribute
Contributing to this project is quite simple & straight forward. We'd request you to view our `contribution.md` file before getting started and follow our `code of conduct`, both of which can be viewed <a href="https://github.com/GoodMorninTech/GoodMorningTech/blob/master/CODE_OF_CONDUCT.md">here</a>.

### Setting up on your local machine
<details>
  <summary>Everything required to set this project up:</summary>
  
  
  #### Cloning the repository
  Clone the repository:
  ```
  git clone https://github.com/GoodMorninTech/GoodMorningTech.git
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
  ```
  mv config.py.template instance/config.py
  ```
  Edit the configuration file and make sure to set the following fields:
  - `SECRET_KEY`
  - `MAIL_USERNAME`
  - `MAIL_PASSWORD`
  - `MAIL_DEFAULT_SENDER`

  Alternatively you can configure everything from environment variables, make sure to set all the variables in `config.py.template`.
  #### Running the Server
  Install the requirements:
  ```
  pip install -r requirements.txt
  ```
  Run the application:
  ```
  python index.py
  ```
  #### Set Up for Development
  Install the development requirements:
  ```
  pip install -r requirements-dev.txt
  ```
  ```
  npm install
  ```
  #### Install pre-commit hooks:
  ```
  pre-commit install
  ```
</details>

## What's Planned Ahead:
- [x] Time Selection
- [x] Timezone Selection
- [x] Addition of more news sources
- [ ] Blogging System
- [ ] Changelog System
- [ ] Support for Other Languages
    - [ ] French
    - [ ] German
    - [ ] Spanish
- [ ] Mobile App

## Frequently Asked Question's (FAQs):

#### 1. How does this work?

It gets the important posts from New York Times, Verge & other credible sources and sends them to your email.

#### 2. How do I subscribe?

Subscribing is as easy as heading to our [sign up page](https://goodmorningtech.news/register) and giving us your email & filling a small form (we promise we won't flood your inbox).

#### 3. How do I unsubscribe?

We hate to see you leave, you can head to [this page](https://goodmorningtech.news/leave) and enter your email ID, we'll then send you a link to verify your exit. Alternatively, each newsletter we send you has a footer with an unsubscribe link.

#### 4. How do you guys fund your project if its completely free?
We rely on donations/sponsors!

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Contact Us
<a align="center" href="https://twitter.com/goodmorningtech">![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)</a>
  <a align="center" href="https://instagram.com/news_goodmorningtech">![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)</a>
  <a align="center" href="https://example.com">![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)</a>


## Authors
### Main Authors:
- [OpenSourceSimon](https://github.com/OpenSourceSimon) - Backend
- [Kappq](https://github.com/kappq) - Backend
- [ImmaHarry](https://github.com/immaharry) - Site Designer & Frontend
- [LevaniVashadze](https://github.com/LevaniVashadze) - Backend & Frontend
### Contributors:
- [Electro199](https://github.com/electro199)
