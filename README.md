1. Установите pyenv
```bash 
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc 
```

2. Установить необходимую версию питона
```bash
make python
```

3. Создать окружение
```bash
make venv
```

4. Поставить поетри
```bash
make poetry
```

5. Инициализация poetry в проекте (выполнять только если нет pyproject.toml)
```bash
poetry init
```

6. Создание структуры проекта (выполнять только если структуры еще нет)
```bash
make struct 
```

Правильно добавлять `torch` через `poetry`
```
poetry add torch --platform linux --python 3.9.13
```

Пример для click
```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    hello()
```

Config Hydra
```python
[hydra]
    enabled = true
    config_dir = configs
    config_name = baseline_hydra.yaml
```