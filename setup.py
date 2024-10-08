from setuptools import setup, find_packages


def parse_requirements():
    with open("requirements.txt", "r") as requirements:
        return requirements.read().splitlines()


setup(
    name='orderbook_handler',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements(),
    description='Orderbook data handler package',
    author='Leo Martinez',
    author_email='leojmartinez@proton.me',
    url='https://github.com/thecheetahcat/orderbook-handler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
