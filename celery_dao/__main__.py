from .app import create_app
from .utils import setup_db
def main():
    setup_db()
    app = create_app()
    app.run(port=8000, host="0.0.0.0")

if __name__ == '__main__':
    main()