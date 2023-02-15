# Bulletin

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/release/python-390/)
![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
_____
[![Bulletin CI](https://github.com/ibrahimroshdy/bulletin/actions/workflows/docker-image.yml/badge.svg)](https://github.com/ibrahimroshdy/bulletin/actions/workflows/docker-image.yml)
[![Python](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
[![Docker](https://img.shields.io/badge/docker-v20.10.12-blue)]()
[![Docker Compose](https://img.shields.io/badge/docker--compose-v1.25.0-blue)]()
[![codecov](https://codecov.io/gh/ibrahimroshdy/bulletin/branch/develop/graph/badge.svg?token=8DZIGQFIPG)](https://codecov.io/gh/ibrahimroshdy/bulletin)

[//]: # (https://demos.creative-tim.com/black-dashboard-django/docs/1.0/plugins/chart-js.html)

[//]: # ()

[//]: # (https://github.com/arteria/django-background-tasks)

Bulletin is a Django-based project that displays a dashboard integrating several applications, including weather,
internet speed and system information, and automation for Twitter and Slack updates.

## Installation

To run the project locally, please follow these instructions:

1. Clone the repository from GitHub: git clone https://github.com/ibrahimroshdy/bulletin.git
2. Install Docker and docker-compose.
3. Create a .env file at the root of the project directory with the following environment variables:
    - DEBUG (set to True or False)
    - SECRET_KEY (a Django secret key)
4. Run the following command to start the project: `docker-compose up -d`
5. Navigate to http://localhost:8000 in your web browser to view the project.

## Features

Bulletin includes the following features:

- **Dashboard**: A centralized view displaying several useful applications at a glance, including weather information,
  internet speed, system information, and social media automation.
- **Weather**: Displays the current weather information for a specified location using the OpenWeatherMap API.
- **Internet Speed**: Tests and displays the current internet upload and download speeds using the speedtest.net API.
- **System Info**: Displays the current CPU and memory usage using the psutil library.
- **Twitter Automation**: Automates posting tweets to a specified Twitter account using the Tweepy library.
- **Slack Automation**: Automates posting messages to a specified Slack channel using the slack-sdk library.

## License

Bulletin is licensed under the MIT License.