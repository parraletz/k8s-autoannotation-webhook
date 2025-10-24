# webhookmuttating-example Template

A production-ready Platform API implementing Clean Architecture principles with comprehensive testing, dependency injection, and modern Python development practices.

## Architecture Overview

This project follows **Clean Architecture** (also known as Hexagonal Architecture or Ports and Adapters) to ensure maintainability, testability, and separation of concerns.

### Design Patterns Implemented

#### 1. Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│              API Layer                   │
│  (FastAPI routes, schemas, server)      │
├─────────────────────────────────────────┤
│            Application Layer             │
│     (Handlers, Use Cases, DI)          │
├─────────────────────────────────────────┤
│             Domain Layer                 │
│   (Models, Interfaces, Errors)         │
├─────────────────────────────────────────┤
│           Infrastructure Layer           │
│    (Repositories, External APIs)        │
└─────────────────────────────────────────┘
```

**Domain Layer** (`app/domain/`)

- Contains business entities and rules
- Independent of external frameworks
- Defines interfaces (ports) for external dependencies

**Application Layer** (`app/handlers/`)

- Contains use cases and business logic orchestration
- Implements application-specific rules
- Depends only on the domain layer

**Infrastructure Layer** (`app/infra/`)

- Implements domain interfaces
- Contains external dependencies (databases, APIs)
- Framework-specific implementations

**API Layer** (`app/api/`)

- HTTP request/response handling
- Input validation and serialization
- Route definitions and middleware

#### 2. Dependency Injection Pattern

The project uses a custom dependency injection container to manage dependencies and ensure loose coupling:

```python
# app/api/di.py
@dataclass
class Container:
    repository: InMemoryRepository
    add_item_service: AddItem
    list_items_service: ListItems
    get_item_service: GetItem
    delete_item_service: DeleteItem
    update_item_service: UpdateItem

def build_container(reset: bool = False) -> Container:
    repository = InMemoryRepository()
    return Container(
        repository=repository,
        add_item_service=AddItem(repository),
        list_items_service=ListItems(repository),
        get_item_service=GetItem(repository),
        delete_item_service=DeleteItem(repository),
        update_item_service=UpdateItem(repository),
    )
```

#### 3. Repository Pattern

Abstracts data access through interfaces, allowing easy swapping of implementations:

```python
# Domain Interface
class ItemRepository(Protocol):
    def save(self, item: Item) -> None: ...
    def get(self, id: ItemId) -> Optional[Item]: ...
    def list_all(self) -> Iterable[Item]: ...
    def delete(self, id: ItemId) -> bool: ...
    def update(self, item: Item) -> None: ...

# Infrastructure Implementation
class InMemoryRepository:
    def __init__(self) -> None:
        self.data: Dict[ItemId, Item] = {}

    def save(self, item: Item) -> None:
        self.data[item.id] = item
```

#### 4. Command/Query Separation

Handlers separate read and write operations:

```python
# Command (Write)
class AddItem:
    def execute(self, id: str, name: str, description: str, price: float) -> Item:
        # Business logic for creating items

# Query (Read)
class GetItem:
    def execute(self, id: ItemId) -> Item:
        # Business logic for retrieving items
```

## Project Structure

```
app/
├── api/                    # API Layer
│   ├── di.py              # Dependency Injection Container
│   ├── routes/            # HTTP Route Handlers
│   │   └── item.py        # Item-related endpoints
│   ├── schemas.py         # Request/Response Models
│   └── server.py          # FastAPI Application Setup
├── domain/                # Domain Layer
│   ├── errors.py          # Domain-specific Exceptions
│   ├── interfaces.py      # Repository Interfaces (Ports)
│   └── models.py          # Domain Entities
├── handlers/              # Application Layer
│   └── item.py            # Use Case Handlers
├── infra/                 # Infrastructure Layer
│   └── memory_repo.py     # Repository Implementation
└── tools/                 # Shared Utilities
    └── validator.py       # Validation Helpers

tests/
├── conftest.py            # Test Configuration
├── test_api_items.py      # Integration Tests
└── test_handlers.py       # Unit Tests
```

## API Examples

### Create Item

```bash
POST /items
Content-Type: application/json

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99
}
```

Response:

```json
{
  "id": "42",
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "created_at": "2025-10-19T20:00:00Z",
  "updated_at": "2025-10-19T20:00:00Z"
}
```

### List Items

```bash
GET /items
```

Response:

```json
[
  {
    "id": "42",
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "created_at": "2025-10-19T20:00:00Z",
    "updated_at": "2025-10-19T20:00:00Z"
  }
]
```

### Get Item by ID

```bash
GET /items/42
```

### Partial Update (PATCH)

```bash
PATCH /items/42
Content-Type: application/json

{
  "price": 899.99
}
```

Only the specified fields are updated, others remain unchanged.

### Delete Item

```bash
DELETE /items/42
```

## Getting Started

### Prerequisites

- Python 3.12+
- uv (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd fastapi-template
```

2. Install dependencies:

```bash
make install
# or
uv sync
```

### Running the Application

#### Development Mode

```bash
make run
# or
ENVIRONMENT=local uv run python main.py
```

#### Production Mode

```bash
make run-prod
# or
uv run python main.py
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## Testing

### Run Tests

```bash
make test
# or
./run_tests.sh
```

### Coverage Reports

```bash
make coverage-report
# or
./coverage_report.sh
```

Current test coverage: **93.88%**

See [TESTING.md](TESTING.md) for detailed testing information.

## Development Commands

The project includes a Makefile with common development tasks:

```bash
make help           # Show available commands
make install        # Install dependencies
make test           # Run tests
make coverage       # Run tests with coverage
make coverage-html  # Generate HTML coverage report
make run            # Start development server
make run-prod       # Start production server
make clean          # Clean up generated files
```

## Benefits of This Architecture

### Testability

- Business logic is isolated and easily testable
- Dependencies can be mocked or stubbed
- Fast unit tests without external dependencies

### Maintainability

- Clear separation of concerns
- Changes in one layer don't affect others
- Easy to understand and modify

### Flexibility

- Easy to swap implementations (e.g., database providers)
- Framework-agnostic business logic
- Supports different deployment scenarios

### Scalability

- Modular design supports team development
- Easy to add new features without breaking existing code
- Clear boundaries for microservice extraction

## Adding New Features

### 1. Define Domain Entity

```python
# app/domain/models.py
@dataclass(frozen=True)
class NewEntity:
    id: EntityId
    name: str
    # ... other fields
```

### 2. Create Repository Interface

```python
# app/domain/interfaces.py
class NewEntityRepository(Protocol):
    def save(self, entity: NewEntity) -> None: ...
    # ... other methods
```

### 3. Implement Repository

```python
# app/infra/new_entity_repo.py
class InMemoryNewEntityRepository:
    def save(self, entity: NewEntity) -> None:
        # Implementation
```

### 4. Create Handlers

```python
# app/handlers/new_entity.py
class AddNewEntity:
    def __init__(self, repository: NewEntityRepository):
        self.repository = repository

    def execute(self, ...) -> NewEntity:
        # Business logic
```

### 5. Add API Routes

```python
# app/api/routes/new_entity.py
def get_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/new-entities")

    @router.post("/")
    def create_entity(body: NewEntityRequest):
        # Route implementation
```

### 6. Update Dependency Container

```python
# app/api/di.py
@dataclass
class Container:
    # ... existing dependencies
    new_entity_repository: NewEntityRepository
    add_new_entity_service: AddNewEntity
```

## Configuration

### Environment Variables

- `ENVIRONMENT`: Set to "local" for development mode with hot reload

### Application Settings

Modify `main.py` to adjust server configuration:

```python
if __name__ == "__main__":
    if os.getenv("ENVIRONMENT") == "local":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
```

## Contributing

1. Follow the established architecture patterns
2. Write tests for new features
3. Maintain test coverage above 90%
4. Update documentation for significant changes
5. Use type hints throughout the codebase

## License

This project is licensed under the MIT License.
