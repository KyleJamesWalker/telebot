try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()

requirements = [
    "pyTelegramBotAPI",
    "requests",
]

test_requirements = [
    "mock",
    "nose",
    "pytest",
    "pytest-mock",
    "vcrpy",
]

setup(
    name='telebot_router',
    version='0.0.6',
    description='A Telegram bot library, with simple route decorators.',
    long_description=readme,
    author='Kyle James Walker',
    author_email='KyleJamesWalker@gmail.com',
    url='https://github.com/KyleJamesWalker/telebot',
    packages=['telebot_router'],
    package_dir={'telebot_router':
                 'telebot_router'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=test_requirements
)
