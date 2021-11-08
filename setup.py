from setuptools import setup

setup(
    name='bulding_NBA_database',
    version='0.1.0',
    py_modules=['retrieve_player_stats'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'get_player_stats = entry_point:get_player_stats'
        ]
    },
)
