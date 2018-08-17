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
docker-compose up --build
```

_Visit localhost:8000 in your browser_

## Development workflow

1. Create a super user for admin access

```bash
docker-compose run --rm web python3 manage.py createsuperuser
```
2. Load fixture data

```bash
docker-compose run --rm web python3 manage.py loaddata starlight/fixtures/fixtures.json
```

3. Develop

4. Apply migrations

```bash
docker-compose run --rm web python3 manage.py makemigrations
docker-compose run --rm web python3 manage.py migrate
```
## Testing

From the root directory, execute:

```
tox
```

