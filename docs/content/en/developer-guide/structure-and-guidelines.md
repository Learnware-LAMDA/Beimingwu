# Project Structure and Guidelines

The Beimingwu system adopts a `Monorepo` code management approach, and the [code repository](https://github.com/Learnware-LAMDA/Beiming-System) contains four sub-projects:
- **Frontend**: Provides the interface and functionality for user interaction with the learnware dock system, including the main system and administrator system.
- **Backend**: Responsible for handling dock system's operation logic and data operations, ensuring system stability and high performance.
- **Docs**: Maintains system documentation, including user guides, development guides, etc., ensuring system usability.
- **Deploy**: Manages the system deployment configuration, including frontend and backend deployment files.

The following sections detail the specific structure and development standards of the entire project.

## Project Structure

The project is divided into four sub-projects: frontend, backend, deploy, and docs, each independent of the others.

### Frontend Project Structure
```shell
├── frontend # Frontend project
    ├── README.md # Frontend documentation
    ├── packages 
    │   ├── admin # Admin module
    │   │   ├── README.md
    │   │   ├── index.html
    │   │   ├── package.json
    │   │   ├── postcss.config.js
    │   │   ├── public # Images
    │   │   ├── src # Code
    │   ├── hooks # Commit checks
    │   ├── locale # Language switching 
    │   │   ├── package.json
    │   │   ├── src
    │   │   │   ├── en # English text
    │   │   │   ├── index.ts
    │   │   │   └── zh-cn # Chinese text
    │   │   ├── tsconfig.json
    │   │   └── tsup.config.ts
    │   ├── main # Frontend module
    │   │   ├── index.html
    │   │   ├── package.json
    │   │   ├── postcss.config.js
    │   │   ├── public # Images
    │   │   ├── src # Code
    │   │   └── vite.config.ts # Project configuration
    │   └── types # Common frontend types
```

### Backend Project Structure

```shell
├── backend # Backend project
    ├── README.md # Backend documentation
    ├── config.py # Backend configuration
    ├── context.py # Backend global variables
    ├── database # Database directory
    │   ├── __init__.py
    │   ├── base.py  # Database base class
    │   └── sqlalchemy.py # Database implementation based on sqlalchemy
    ├── lib # Various tools
    │   ├── command_executor.py # Command line
    │   ├── common_utils.py # General
    │   ├── data_utils.py # Data
    │   ├── database_operations.py # Database operations
    │   ├── engine.py # Learnware engine tools
    │   └── redis_utils.py # Redis
    ├── requirements.txt # 
    ├── restful # Web APIs
    │   ├── admin.py # Admin APIs
    │   ├── auth.py # User authentication
    │   ├── common_functions.py # General functions
    │   ├── engine.py # Engine APIs
    │   ├── user.py # User operation APIs
    │   └── utils.py # Utility functions, such as sending emails
    ├── scripts # Various scripts
    │   ├── backup_data.py # Data backup
    │   ├── main.py # Web entry
    │   └── monitor_learnware_verify.py # Learnware verification
    ├── tests # Test cases
        ├── common_test_operations.py # General test functions
        ├── data  # Data for test
        ├── stress_test # Stress test
        ├── test_admin.py # Test for Admin APIs
        ├── test_auth.py # Test for user authentication
        ├── test_backup_data.py # Test for data backup
        ├── test_command_executor.py # Test for command execution
        ├── test_engine.py # Test for engine APIs
        ├── test_learnware_client.py # Test for Learnware client
        ├── test_monitor_learnware_verify.py # Test for monitor_learnware_verify.py
        ├── test_user.py # Test for user APIs
        └── test_verify_learnware.py # Test for single learnware verification
```

### System Deployment Project Structure

```shell
├── deploy # System deployment project
    ├── docker-compose # Docker deployment files
    │   └── docker-compose.yaml
    ├── hooks # Git commit checks
    │   ├── commit-msg # Commit message check
    │   └── pre-commit # Code check
    ├── kubernetes # Kubernetes deployment 
    │   ├── admin-frontend.yaml # Admin configuration
    │   ├── backend.yaml # Backend deployment configuration
    │   └── frontend.yaml # Frontend deployment configuration
    └── static # Static files
        └── learnware-template # Learnware template
```

### System Documentation Project Structure

```shell
├── docs # System documentation project
    ├── README.md # Documentation service description
    ├── content 
    │   ├── public # Images
    │   ├── en # English documentation
    │   ├── zh-CN # Chinese documentation
    │   └── tsconfig.json # Project configuration
```

## Development Standards

As we use a `Monorepo` code management approach, standardizing `commit` formats and project development standards is very important. The following text will mainly introduce `hooks` configuration, code submission standards, and frontend and backend development standards.

### `hooks` Configuration

The project is configured with `hooks`, as follows:
- `commit-msg`: Restricts commit format;
- `pre-commit`: Automatically formats code before commit.

To make `hooks` effective, execute the following command in the project root directory:
```shell
git config core.hooksPath deploy/hooks
```
For Linux systems, additional permissions are required:
```shell
chmod +x deploy/hooks/*
```

### Code Submission Standards

The `commit` format for the Beimingwu project is: `<type>`(`<scope>`): `<subject>`
- `<type>` must be one of the following:
    - feat: Add new feature
    - fix: Fix a bug
    - docs: Modify documents, such as README, CHANGELOG, etc.
    - style: Modify format, including comments, code format, commas, etc., without affecting code execution
    - refactor: Code refactoring, no new features or bug fixes
    - perf: Code optimization, such as performance, experience enhancement
    - test: Test cases, including unit tests, integration tests, etc.
    - chore: Changes to the build process, or adding dependencies, tools, etc.
    - revert: Revert to a previous version
- `<scope>` has the following options: frontend, backend, docs, deploy
    - If multiple scopes are involved, use commas to connect, or simply use *
- `<subject>` must be filled in, all in lowercase English

For example, the following are all valid:
```shell
feat(backend): add the modify learnware api
fix(frontend,backend): fix email verification
docs(*): update README
```

### Backend Development Standards

When developing the backend sub-project, certain standards need to be followed, mainly involving web interfaces, databases, exception handling, and testing.

#### Web Interface Standards

Web interfaces are uniformly developed using the `flask-restx` framework. Each interface needs to define a `parser`, allowing automatic generation of `swagger` documentation.

URL interfaces are uniformly added at the end of the file using `add_resource`.

Interfaces by default return JSON strings. The returned `http code` is 200, and the JSON string must contain `code` and `msg` keywords. `code` is a business code, generally 0 represents success, and `msg` is the message. If there is additional information, it can be placed in the `data` field.

#### Database Standards

The database is developed using the `SQLAlchemy` library. Database tables are defined using `sqlalchemy.ext.declarative`. Data storage and retrieval are handled using `raw sql`. The `sql` statements must comply with both `sqlite` and `postgres` standards.

#### Exception Handling Standards

Exceptions caught by the backend should be logged using the `logger.exception` method.

Business exceptions should be caught and handled by setting the appropriate `code` and `msg` in the returned JSON. For system exceptions, uniformly return `http code 500`.

#### Testing Standards

Each web interface requires corresponding unit test cases. In the test cases, start a simulated backend for mock calls and then check the return value.

General testing logic (such as clearing the database, registering a user, etc.) is placed in `common_test_operations.py`.