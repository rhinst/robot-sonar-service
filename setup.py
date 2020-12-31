from setuptools import setup
import platform


setup(
  name='robot-sonar-service',
  version='0.1',
  description='Robot sonar service',
  url='https://github.com/rhinst/robot-sonar-service',
  author='Rob Hinst',
  author_email='rob@hinst.net',
  license='MIT',
  packages=['sonar'],
  install_requires = [
    'redis==3.5.3',
    'himl==0.7.0',
    'RPi.GPIO==0.7.0' if platform.platform().lower().find("armv71") > -1 else 'Mock.GPIO==0.1.7',
  ],
  test_suite='tests',
  tests_require=['pytest'],
  entry_points={
    'console_scripts': ['sonar=sonar']
  }
)