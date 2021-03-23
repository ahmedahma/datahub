from setuptools import setup

setup(name='proto',
      version='0.0.1',
      description='Datapipeline http server prototype',
      url='git@gitlab.com:asaboni/stproto.git',
      author='Amine Saboni',
      author_email='amine.saboni@octo.com',
      packages=['proto'],
      install_requires=[
            'fastapi',
            'uvicorn',
            'airflow',
            'numpy'
      ],
      test_requirments=[
            'pytest',
            'pytest-cov',
            'great_expectations',
            'tox'
      ],
      zip_safe=False)
