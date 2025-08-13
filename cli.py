import click
import requests
import sys
import os
from datetime import datetime, timedelta
TOKEN_FILE = ".mycli_token"
@click.group()
def cli():
    """CLI pentru operații matematice (pow, fibonacci, factorial)"""
    pass
def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token.strip())
def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()

def get_auth_headers():
    token = load_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}
@click.command()
@click.argument('file', type=click.File('r'))
def read_file(file):
    content = file.read()
    response = requests.get(f"http://127.0.0.1:8000/file/{file.name}", headers=get_auth_headers())
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")

@click.command()
@click.argument('fibonacci_number', type=int)
def fibonacci(fibonacci_number):
    if fibonacci_number < 0:
        click.echo("Error: Fibonacci number must be a non-negative integer.")
        sys.exit(1)
    if fibonacci_number > 100:
        click.echo("Error: Fibonacci number is too large (max 100).")
        sys.exit(1)
    response = requests.get(f"http://127.0.0.1:8000/n-th_fibonacci/{fibonacci_number}", headers=get_auth_headers())
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")

@click.command()
@click.argument('base', type=float)
@click.argument('exponent', type=float)
def pow(base, exponent):
    if base > 100 or exponent > 100:
        click.echo("Error: Base and exponent must be <= 100.")
        sys.exit(1)
    params = {"base": base, "exponent": exponent}
    response = requests.get("http://127.0.0.1:8000/pow", params=params, headers=get_auth_headers())
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")

@click.command()
@click.argument('number', type=int)
def factorial(number):
    if number < 0:
        click.echo("Error: Factorial number must be a non-negative integer.")
        sys.exit(1)
    if number > 40:
        click.echo("Error: Factorial number is too large (max 40).")
        sys.exit(1)
    response = requests.get(f"http://127.0.0.1:8000/factorial/{number}", headers=get_auth_headers())
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")

@click.command()
@click.argument('name')
@click.argument('password')
def login(name, password):
    response = requests.post("http://127.0.0.1:8000/login", json={"name": name, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        save_token(token)
        click.echo("Login successful.")
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")
@click.command()
@click.argument('name')
@click.argument('password')
def signup(name, password):
    response = requests.post("http://127.0.0.1:8000/signup", json={"name": name, "password": password}, headers=get_auth_headers())
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.status_code} - {response.text}")

@click.command()
def logout():
    try:
        os.remove(TOKEN_FILE)
        click.echo("Logout successful.")
    except FileNotFoundError:
        click.echo("Already logged out.")
    
cli.add_command(logout)
cli.add_command(login)
cli.add_command(signup)
cli.add_command(pow)
cli.add_command(factorial)
cli.add_command(fibonacci)
cli.add_command(read_file)

if __name__ == '__main__':
    cli()