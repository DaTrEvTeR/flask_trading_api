# **Flask Trading Api**

---

#### This project was developed as a test task for B&G Soft Agency

---

## ▶️ Run

To run an application from scratch in multi-container mode use the following command:

```shell
docker compose --profile full_dev up --build
```

## 🛠️ Dev

Make sure you have [Poetry](https://python-poetry.org/) installed. To install all project dependencies, run:

```shell
poetry install --no-root
```

Activate environment shell by:

```shell
poetry shell
```

This project uses postgresql, rabbitMQ and redis to run.
To run these services via docker compose separately from the application, use the following commands:

```shell
docker compose --profile local_dev up --build
```

and then run the application

```shell
python main.py
```

## author

### Mykhailo Rozhkov

[LinkedIn](https://github.com/DaTrEvTeR)  
[Telegram](https://t.me/datrevter)  
Email: rozhkovm176@gmail.com
