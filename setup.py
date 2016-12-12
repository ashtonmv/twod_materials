from setuptools import setup, find_packages


setup(
  name = 'twod_materials',
  packages = find_packages(),
  include_package_data = True,
  version = '0.0.4',
  install_requires = ['monty>=0.7.2', 'matplotlib>=1.4.2', 'nose>=1.3',
                      'scipy==0.14.0', 'pymatgen==4.2.0'],
  extras_require = {'doc': ['codecov>=2.0', 'sphinx>=1.3.1']},
  license = 'GNU',
  description = 'High throughput 2D material modules',
  author = 'Michael Ashton',
  author_email = 'mashton@ufl.edu',
  url = 'https://github.com/ashtonmv/twod_materials',
  download_url = 'https://github.com/ashtonmv/twod_materials/tarball/0.0.4',
)
