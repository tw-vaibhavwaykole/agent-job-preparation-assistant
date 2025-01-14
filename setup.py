from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="job-prep-assistant",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A job preparation and placement assistant web application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/job-prep-assistant",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=2.0.1',
        'flask-sqlalchemy>=2.5.1',
        'flask-login>=0.5.0',
        'flask-bcrypt>=0.7.1',
        'anthropic>=0.3.0',
        'python-dotenv>=0.19.0',
        'reportlab>=3.6.8',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'job-prep-assistant=app:create_app',
        ],
    },
) 