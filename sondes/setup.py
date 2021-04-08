from setuptools import setup

setup(name='sondes',
      version='0.0.1',
      description='Metadata ingestion',
      url='git@gitlab.com:asaboni/tdf_innovation.git',
      author='Amine Saboni, Ahmed Alaoui',
      author_email='amine.saboni@octo.com, a.alaoui.abdallaoui@octo.com',
      packages=['src'],
      install_requires=[
            'fastapi',
            'uvicorn',
            'apache-airflow',
            'pandas',
            'numpy',
            'datahub'
      ],
      zip_safe=False)
