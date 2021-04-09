import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="trello_client-basics-api-denisshvayko", version="0.0.1", author="denis", author_email="denis.shvayko@phystech.edu",
    description="Обертка для trello API", long_description=long_description,
    long_description_content_type="text/markdown", url="https://github.com/denisshvayko/D1.8.git",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent", ], python_requires='>=3.6', )