# Creador de estructruras básicas de proyectos

Este proyecto busca ser un generador de proyectos con una estructura básica general permitiendo tener un patrón entre los distintos proyectos creados.

```
proyecto/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── database.py
│   │   └── logging_config.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── extractors/
│   │   │   ├── __init__.py
│   │   │   ├── base_extractor.py
│   │   │   ├── mongodb_extractor.py
│   │   │   ├── api_extractor.py
│   │   │   └── file_extractor.py
│   │   ├── transformers/
│   │   │   ├── __init__.py
│   │   │   ├── base_transformer.py
│   │   │   ├── data_cleaner.py
│   │   │   └── data_validator.py
│   │   └── loaders/
│   │       ├── __init__.py
│   │       ├── base_loader.py
│   │       ├── mongodb_loader.py
│   │       └── csv_loader.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── exceptions.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── google_sheets_service.py
│   │   ├── mongodb_service.py
│   │   └── email_service.py
│   └── tests/
│       ├── __init__.py
│       ├── test_extractors/
│       ├── test_transformers/
│       └── test_utils/
├── notebooks/ (opcional, para exploración)
├── docs/
├── scripts/
│   ├── setup_database.py
│   └── deploy.py
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── docker-compose.yml
└── Dockerfile
```

## Carpetas y archivos por servicios:

### Mongodb:
#### Carpeta data:
```
./src/data/extractors/mongodb_extractor.py
./src/data/loaders/mongodb_loader.py
./src/data/transformers/mongodb_transformer.py
```

#### Carpeta services
```
./src/services/mongodb_service.py
```

### Google sheets:
#### Carpeta Data
```
./src/data/extractors/google_sheets_extractor.py
./src/data/loaders/google_sheets_loader.py
./src/data/transformers/google_sheets_transformer.py
```


#### Carpeta config
```
./config/google_sheet_config.yaml
```














