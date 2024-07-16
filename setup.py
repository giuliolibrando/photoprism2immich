# setup.py

from setuptools import setup, find_packages

setup(
    name='photoprism2immich',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        # Altre dipendenze se necessario
    ],
    entry_points={
        'console_scripts': [
            'photoprism2immich = photoprism2immich.photoprism2immich:main',
        ],
    },
    author='Giulio Librando',
    author_email='giuliolibrando@gmail.com',
    description='Tool to migrate Photoprism library to Immich',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/giuliolibrando/photoprism2immich',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
