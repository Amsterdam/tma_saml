from setuptools import setup

setup(name='tma_saml',
      version='0.4.3',
      description='TMA SAML processing package',
      url='https://github.com/Amsterdam/tma_saml/',
      author='DataPunt',
      author_email='datapunt@amsterdam.nl',
      license='MIT',
      packages=['tma_saml', 'tma_saml.for_tests'],
      install_requires=[
          'signxml>=2.6.0',
          'Flask>=1.1.1',
          'lxml>=4.3.4',
          'python-dateutil'
      ],
      setup_requires=['pytest-runner', ],
      tests_require=['pytest', ],
      zip_safe=False)
