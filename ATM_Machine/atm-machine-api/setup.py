from setuptools import setup, find_packages

setup(
    name="atm-machine-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
        "pydantic>=2.6.1",
        "python-multipart>=0.0.9",
        "sqlalchemy>=2.0.25",
        "alembic>=1.13.1",
        "psycopg2-binary>=2.9.9",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-dotenv>=1.0.1",
        "typing-extensions>=4.8.0",
    ],
    python_requires=">=3.8",
) 