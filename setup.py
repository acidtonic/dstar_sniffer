from setuptools import setup, find_packages

setup(name='DStarSniffer',
      version='1.0',
      description='DStar repeater controller sniffer',
      url='http://github.com/elielsardanons/dstar-sniffer',
      author='Eliel Sardanons LU1ALY',
      author_email='eliel@eliel.com.ar',
      license='MIT',
      packages=find_packages(),
      keywords='hamradio dstar aprs icom kenwood d74',
      install_requires=[
          'aprslib',
          'jinja2',
      ],
      include_package_data=True,
      package_data={'/' : ['dstar_sniffer/config/*.conf',]},
      data_files=[
		('/etc/dstar_sniffer',
			[
			'dstar_sniffer/config/dstar_sniffer.conf',
			'dstar_sniffer/config/logging.conf',
			'dstar_sniffer/config/last_heard.html',
			 ])
      ],
      entry_points={
        'console_scripts': [
            'dstar_sniffer=dstar_sniffer.dstar_sniffer:main',
        ],
      }
)
