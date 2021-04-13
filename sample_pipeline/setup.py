from setuptools import setup

setup(name='sample_pipeline',
      version='0.0.1',
      description='Datapipeline http server prototype',
      url='git@gitlab.com:asaboni/stproto.git',
      author='Amine Saboni',
      author_email='amine.saboni@octo.com',
      packages=['sample_pipeline'],
      install_requires=[
            'fastapi',
            'numpy',
            'pandas',
            'uvicorn',
            'mlflow',
            'sklearn'
      ],
      zip_safe=False)
