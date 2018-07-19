# starlight
Cross-functional skill tracking system for Agile teams. 🌟

## Installation

Required packages:
* git
* Docker
* docker-compose

```bash
git clone https://github.com/savoirfairelinux/starlight.git
cd starlight
cp .env.json.example .env.json
python3 manage.py loaddata starlight/fixtures/fixtures.json
docker-compose up --build
```

_Visit localhost:8000 in your browser_

## Development workflow

1. Create a super user for admin access

```bash
docker exec -it starlight_web1 python3 manage.py createsuperuser
```

2. Develop

3. Apply migrations

```bash
docker exec -it starlight_web1 python3 manage.py makemigrations
docker exec -it starlight_web1 python3 manage.py migrate
