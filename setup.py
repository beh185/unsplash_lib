# Github: https://github.com/beh185
# Telegram: https://T.me/dr_xz
# e-mail: BehnamH.dev@gmail.com
# ____________________________________________

from setuptools import setup, find_packages

with open(__file__.replace('setup.py', 'README.md'), 'r') as f:
    long_description = f.read()

setup(
        name="unsplash_downloader",
        version='0.0.2',
        description='A python library that can download from unsplash and also mange user account',
        long_description=long_description,
        author='Behnam',
        author_email='Behii@tutanota.com',
        url='https://github.com/beh185/unsplash_downloader',
        license='MIT',
        keywords='download from unsplash',
        packages=find_packages(),
        include_package_data=True,                                                  
        install_requires=['requests', 'tqdm'],
        python_requires='~=3.7',
        classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
        )