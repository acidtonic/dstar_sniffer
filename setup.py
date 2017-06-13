from setuptools import setup, find_packages
from glob import glob

setup(name='DStarSniffer',
      version='0.1',
      description='DStar repeater controller sniffer',
      url='http://github.com/elielsardanons/dstar-sniffer',
      author='Eliel Sardanons LU1ALY',
      author_email='eliel@eliel.com.ar',
      license='MIT',
      packages=find_packages(),
      keywords='hamradio dstar aprs icom kenwood d74',
      install_requires=[
          'aprslib',
      ],
      data_files=[('/etc/dstar_sniffer', glob("config/*.conf"))],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'dstar_sniffer=dstar_sniffer.dstar_sniffer:main',
        ],
      }
)
