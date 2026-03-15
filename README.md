# 🚀 FastAPI CRUD API with Docker

A simple **CRUD API built using FastAPI**, containerized with **Docker and Docker Compose** for quick setup and consistent development environments.

---

## 📌 Features

* ⚡ FastAPI based REST API
* ✨ CRUD Operations (Create, Read, Update, Delete)
* 🐳 Dockerized project for easy deployment
* 📦 Docker Compose for managing services
* 📖 Interactive API documentation with Swagger

---

## 🛠 Tech Stack

* **FastAPI**
* **Python**
* **Docker**
* **Docker Compose**
* **REST API**

---

## 📂 Project Structure

```
project-root/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup and Run the Project

## 1️⃣ Install Docker Desktop

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

After installation, start Docker Desktop and make sure it is running.

---

## 2️⃣ Clone the Repository

```bash
git clone https://github.com/Shikha4554/FastApi-Project.git
cd FastApi-Project.
```

---

## 3️⃣ Run the Project (First Time)

For the first time, you need to build the Docker image.

```bash
docker compose up --build
```

This command will:

* Build the Docker image
* Install all dependencies
* Start the FastAPI server

---

## 4️⃣ Run the Project (Next Time)

After the first build, you can run the project using:

```bash
docker compose up
```

---

## 🌐 Access the API

Once the container is running, open the following in your browser.

### Base URL

```
http://localhost:8000
```

### Swagger API Documentation

```
http://localhost:8000/docs
```

### ReDoc Documentation

```
http://localhost:8000/redoc
```

---

## 🧪 Example CRUD Endpoints

| Method | Endpoint    | Description       |
| ------ | ----------- | ----------------- |
| POST   | /items      | Create a new item |
| GET    | /items      | Get all items     |
| GET    | /items/{id} | Get item by ID    |
| PUT    | /items/{id} | Update item       |
| DELETE | /items/{id} | Delete item       |

---

## 🛑 Stop the Containers

To stop the running containers:

```bash
docker compose down
```

---

## 👩‍💻 Author

**Shikha Singh**

* Python Backend Developer
* FastAPI | Django | Machine Learning

---

⭐ If you like this project, consider giving it a **star on GitHub**.
