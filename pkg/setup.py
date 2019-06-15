import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyweaver",
    version="0.0.1",
    author="Example Author",
    author_email="francisco.leskovar@gmail.com",
    description="Web based Python visual programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fleskovar/PyWeaver",
    download_url = 'https://github.com/fleskovar/PyWeaver/archive/v0.0.1.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
	scripts=['bin/pyweaver.bat', 'bin/pyweaver-main.py'],
    install_requires=[
          'flask',
          'flask_socketio',
          'numpy',
          'xmltodict'
      ],
)