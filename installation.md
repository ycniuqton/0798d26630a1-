# 🚀 ResellVPS Installation Guide

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://docs.docker.com/get-docker/)
[![Nginx](https://img.shields.io/badge/nginx-stable-green.svg)](https://nginx.org/)

This guide will walk you through the complete installation process of the ResellVPS system.

---

## 📋 Table of Contents
- [System Prerequisites](#system-prerequisites)
- [Docker Setup](#docker-setup)
- [Nginx and SSL Setup](#nginx-and-ssl-setup)
- [Environment Configuration](#environment-configuration)
- [Starting the Application](#starting-the-application)
- [Codebase Structure](#codebase-structure)

---

## 💻 1. System Prerequisites

### 🔄 Update System
```bash
apt update && apt upgrade
```

### 📥 Pull Code
```bash
git clone git@github.com:ycniuqton/0798d26630a1-.git vps-web
cd vps-web
```

### 🐍 Install Python Environment
```bash
pip install pipenv --force
apt install pipenv
```

### 🔧 Setup Virtual Environment
```bash
pipenv shell
git checkout dev/user
pip install -r requirements.txt

```

---

## 🐳 2. Docker Setup

### 📦 Install Docker
```bash
apt install docker.io install docker-compose -y

```

### ⚙️ VPS docker-requirements
create vps folder then copy  vps.yaml to vps folder

```bash
mkdir vps
cp vps.yaml vps/

docker-compose up --build
```


---

## 🔒 3. Nginx and SSL Setup

### 📌 Install Nginx and Certbot
```bash
apt install nginx certbot python3-certbot-nginx -y

```

### 🛡️ Configure SSL
```bash
sudo certbot --nginx -d resellvps.net
sudo certbot renew --dry-run

```

---

## ⚙️ 4. Environment Configuration

Configure parameters in `env.yaml`:
- 🔑 Set ResellVPS account keys
- 📡 Update Kafka IP for virtualizor events
- 🗄️ Configure database IP
- ⚡ Other necessary parameters




<br />

> Start the APP

```bash
$ python manage.py createsuperuser # create the admin
$ python manage.py makemigrations   # Prepare database migrations
$ python manage.py migrate          # Apply migrations
$ python manage.py runserver        # start the project
```

✨ The application will be available at `http://127.0.0.1:8000/`.

<br />

## 📁 Codebase Structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            # Core Application
   |    |-- settings.py                 # Project Configuration  
   |    |-- urls.py                     # Project Routing
   |
   |-- home/                            # Home Application
   |    |-- views.py                    # APP Views 
   |    |-- urls.py                     # APP Routing
   |    |-- models.py                   # APP Models 
   |    |-- tests.py                    # Tests  
   |    |-- templates/                  # Theme Customisation 
   |         |-- pages/                 # Page Templates
   |              |-- custom-index.py   # Custom Dashboard      
   |
   |-- requirements.txt                 # Project Dependencies
   |-- env.sample                       # ENV Configuration
   |-- manage.py                        # Django Start Script
```

---

📝 **Note**: Make sure to follow each step in order and verify the success of each command before proceeding to the next step.

❓ For any issues or questions, please refer to the project documentation or create an issue in the repository.