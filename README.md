<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Noel-louis/odoo-trip-estimator">
    <img src="static/description/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Odoo-trip-estimator</h3>

  <p align="center">
    Helps you estimate Your travail time in Odoo !
    <br />
    <br />
    <a href="https://github.com/Noel-louis/odoo-trip-estimator/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/Noel-louis/odoo-trip-estimator/issues/new">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This project is a product made for the company IT-SIS. The goal is simple, create a module where we can estimate the distance between us and our client delivery address inside Odoo. We also needed to use an open-source and free solution to calculate the distance

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [Python](https://www.python.org/)
- [OpenRouteService](https://openrouteservice.org/)

Since Odoo is made in python, we used this language for our module.

OpenRouteServce let us calculate easily through their API the distance and time between two points.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Here are the differents steps to install and use this module.

### Prerequisites

For this module to work, you'll need to get an [OpenRouteService APIkey](https://openrouteservice.org/dev/#/home). It is free, open-source and you just need to create an account to use their service.

### Installation

To install this module into Odoo, follow thes steps.

1. Clone the repo inside your Odoo installation addons folder
   ```sh
   git clone https://github.com/Noel-louis/odoo-trip-estimator
   ```
2. Install Python packages for openrouteservice
   ```sh
   pip install -r requirements.txt
   ```
3. Restart your odoo server and upgrade your module list
4. Enter your API in the parameter for the module

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

This module is really simple and easy to use. it adds a button and 2 lines of information on _DELIVERY CONTACT_ only. if the api key is set properly, just press the button and wait a bit for the data to be received, you'll get an estimation of the time and distance between your company address (the one in the general parameter) and the delivery address.

Note that Every request result will be stored in Odoo database and used if possible instead of an API request.

Also, the number of API request is limited in quantity per day but should be more than enough for every use.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Not Yet decided. will come soon.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Feel free to create an issue if you need something

Project Link: [https://github.com/Noel-louis/odoo-trip-estimator](https://github.com/Noel-louis/odoo-trip-estimator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

This project use a list of open-source project which should be looked at if you're curious. They're really great and are really interesting.

- [Open Street Map](https://www.openstreetmap.org)
- [Open Route Service](https://openrouteservice.org)
- [Odoo](https://www.odoo.com)
- [Readme Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
