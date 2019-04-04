import os

from saythanks import app

is_test_run = "TEST" in os.environ

if __name__ == "__main__" and not is_test_run:
    app = app.app
    app.run()


