# image_frames_server/conftest.py
import os


def pytest_configure():
    os.environ["TESTING"] = "True"
