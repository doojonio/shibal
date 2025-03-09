# Shibal

This repository contains the source files for a simple Telegram bot named **ShibalAudio** ([@shibal_wav_bot](https://t.me/shibal_wav_bot)), designed to edit audio files.
The primary goal of this project was not to create something highly practical, but rather to learn new skills and refresh existing ones within a short timeframe.
The current version of the bot was developed in just 4-5 days and should be considered a proof of concept rather than a fully functional tool.
As such, it is still in its early stages and may have limited functionality.

# Contents

The project is organized into four directories:

- **[shibal](https://github.com/doojonio/shibal/tree/main/shibal)**: Contains three services (an admin web server built with FastAPI, celery queue tasks, and a Telegram bot handler) unified under a single codebase.
- **[front_stats](https://github.com/doojonio/shibal/tree/main/front_stats)**: Includes the source code for the admin web server's frontend, developed using Angular 19.
- **[drive](https://github.com/doojonio/shibal/tree/main/drive)**: A lightweight microservice written in Rust, featuring two primary methods: 1) file upload and 2) file download.
- **[nginx](https://github.com/doojonio/shibal/tree/main/nginx)**: Contains configuration files for a local NGINX load balancer, which proxies requests to the API and frontend containers.

# Run

To run the project locally using Docker Compose, you only need a Telegram bot API token. Save the token in the `.env` file, following the format provided in `.env.sample`. Once the token is set, launch the project with the following command:

```bash
docker compose up
```

