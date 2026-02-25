# dbt — ma cantine

Transforms data from the data warehouse into analytics-ready tables and views.

## Architecture

```
Data Warehouse — schema: public           ← source tables (loaded by Python ETL)
      │
      │  dbt
      ▼
Data Warehouse — schema: dbt_dev_staging  ← staging views (dev)
Data Warehouse — schema: dbt_prod_staging ← staging views (prod)
Data Warehouse — schema: dbt_dev_marts    ← mart tables (dev)
Data Warehouse — schema: dbt_prod_marts   ← mart tables (prod)
```

## Setup

### 1. Credentials

Create a `.env` file at the root of the repo (never commit it):

```sh
DATA_WARE_HOUSE_HOST=...
DATA_WARE_HOUSE_USER=...
DATA_WARE_HOUSE_PASSWORD=...
DATA_WARE_HOUSE_PORT=5432
DATA_WARE_HOUSE_DB=...
```

### 2. Install

```sh
uv sync
```

### 3. Test the connection

```sh
cd /path/to/ma-cantine
set -a && source .env && set +a && cd dbt && dbt debug
```

You should see `Connection test: OK`.

## Running dbt

From the repo root:

```sh
make dbt-run        # dev (creates dbt_dev_* schemas)
make dbt-run-prod   # prod (creates dbt_prod_* schemas)
make dbt-test       # run data quality tests
make dbt-docs       # generate and serve documentation
```

## Project structure

```
dbt/
├── profiles.yml              # DB connection config (uses DATA_WARE_HOUSE_* env vars)
├── dbt_project.yml           # project config (schema names, materialization)
├── setup/
│   └── fdw_setup.sql         # one-time FDW setup — run by sysadmin with superuser (not committed)
└── models/
    ├── staging/              # views — thin layer on top of source tables
    │   ├── sources.yml       # source table definitions
    │   ├── schema.yml        # model docs and tests
    │   └── stg_*.sql
    └── marts/                # tables — business logic, ready for Metabase
        └── mart_*.sql
```

## Adding a new model

1. Create a `.sql` file in `models/staging/` or `models/marts/`
2. Reference sources with `{{ source('datawarehouse', 'table_name') }}`
3. Run `make dbt-run` to deploy it
