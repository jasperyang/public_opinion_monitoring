# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'YQ_download',
    version      = '1.0',
    packages     = find_packages(),
    package_data = {
        'YQ_download':['cookies/*']
    },
    scripts = ['YQ_download/spiders/data_processing.py'],
    entry_points = {'scrapy': ['settings = YQ_download.settings']},
    zip_safe = False,
)
