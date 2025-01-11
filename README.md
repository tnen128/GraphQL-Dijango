
# Django Simulator with Airflow Integration

## Description
A Django-based application that manages simulators and KPIs (Key Performance Indicators) with automated task scheduling using Apache Airflow. The application uses GraphQL for API interactions and Docker for containerization. Each simulator generates random values at specified intervals, which are then processed using configured KPI formulas.

## Project Structure
```
simulator_project/
├── airflow/
│   └── dags/
│       └── dynamic_dag_generator.py
│
├── simulator_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── schema.py
│
├── simulator/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── schema.py
│
├── kpis/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── schema.py
│
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── init-db.sql
```
## Prerequisites
- Docker and Docker Compose installed
- Git (optional)
- Python 3.9 or higher (for local development)

## Installation Steps

1. **Clone the repository** (or create project structure):
```bash
git clone https://github.com/tnen128/GraphQL-Dijango.git
cd simulator_project
```


2. **Start the services**:
```bash
docker-compose up -d
```

3. **Apply migrations**:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

4. **Create superuser**:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Usage

### Access Points:
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- GraphQL Interface: [http://localhost:8000/graphql/](http://localhost:8000/graphql/)
- Airflow UI: [http://localhost:8080](http://localhost:8080) (login: admin/admin)


### View Airflow DAGs:
Go to [http://localhost:8080](http://localhost:8080)  
Login with `admin/admin`.  
You should see DAGs created for each simulator.

## Monitoring

### View Django Logs:
```bash
docker-compose logs -f web
```

### View Airflow Logs:
```bash
docker-compose logs -f airflow-scheduler
```

### View DAG Task Logs:
```bash
docker-compose exec airflow-scheduler airflow tasks list-logs simulator_dag_1 generate_and_process_value
```

## GraphQL Operations
#### You will all the queries that can be applied inside Queries.pdf and Queries.txt
## Troubleshooting

### If services don't start:
```bash
docker-compose down -v
docker-compose up --build
```

### If database issues occur:
```bash
docker-compose exec web python manage.py migrate
```

### If DAGs don't appear:
```bash
docker-compose restart airflow-scheduler
```

## Development

### To make changes:

1. Modify code.
2. Restart services:
```bash
docker-compose restart web  # For Django changes
docker-compose restart airflow-scheduler  # For DAG changes
```

## Notes
- KPI formulas use 'x' as the variable (e.g., "x * 2", "x + 5").
- Simulator intervals are in seconds.
- DAGs are automatically created for each simulator.
- All times are in UTC.
