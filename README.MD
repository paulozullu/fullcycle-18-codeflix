# Codeflix Catalog Admin

Este é um projeto de administração de catálogos desenvolvido com Python e Django.

## Requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes do Python)
- Git

## Instalação

- Clone o repositório

```bash
git clone git@github.com:paulozullu/fullcycle-18-codeflix.git
cd codeflix-catalog-admin-zoio
```

- Crie um ambiente virtual

```bash
python -m venv venv
```

- Ative o ambiente virtual
No Linux/Mac:

```bash
source venv/bin/activate
```

No Windows:

```bash
venv\Scripts\activate
```

- Instale as dependências

```bash
pip install -r requirements.txt
```

## Configuração do banco de dados

O projeto está configurado para usar SQLite por padrão, que já está incluído no Python.

Execute as migrações para criar as tabelas do banco de dados:

```bash
python manage.py migrate
```

## Executando o servidor

Para iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará disponível em <http://127.0.0.1:8000/>

## Executando testes

Este projeto utiliza pytest para testes. Para executar todos os testes:

```bash
pytest
```

Para executar testes específicos:

```bash
# Testes
pytest src/
```
