from flask import Flask

from app.entryapp import app


if __name__ == "__main__":
    app.run(port = 5000)