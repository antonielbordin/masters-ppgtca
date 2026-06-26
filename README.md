# masters-tese-PPGTCA
Code creating for masters in PPGTCA

masters_ppgtca/
├── core/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── zone.py          # Entidade Zona de Manejo
│   │   ├── talhao.py        # Entidade Talhão
│   │   └── sample_point.py # Entidade Ponto Amostral
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── zoning.py          # Caso de uso principal
│   │   ├── optimization.py      # Otimização de parâmetros
│   │   └── validation.py       # Validação de resultados
│   └── ports/
│       ├── __init__.py
│       ├── agdatabox_port.py # Interface para AgDataBox
│       ├── algorithm_port.py  # Interface para algoritmo
│       └── repository_port.py # Interface para persistência
│
├── infrastructure/
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── agdatabox_adapter.py    # Implementação concreta
│   │   ├── algorithm_adapter.py    # Algoritmo de zoneamento
│   │   └── repository_memory.py   # Repositório em memória
│   └── external_services/
│       ├── __init__.py
│       ├── geometry.py              # Utilitários geométricos
│       └── clustering.py            # Algoritmos de cluster
│
├── interfaces/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── zoning_controller.py
│   │   └── talhao_controller.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   └── zoning_schema.py
│   └── routes/
│       ├── __init__.py
│       └── api_routes.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   └── integration/
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md