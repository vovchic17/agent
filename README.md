# Агент для поиска лог-файлов

## Инструкция по установке

### Клонируйте репозиторий
```bash
git clone https://github.com/vovchic17/agent.git
```

### Установите директорию лог-файлов и порт приложения в файле .env
```
PORT=8000
AUTH_USERNAME=username
AUTH_PASSWORD=password
```

### Установите пакетный менеджер
```bash
pip install uv
```

### Запустите проект
```bash
uv run agent
```