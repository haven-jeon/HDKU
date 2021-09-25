from setuptools import setup


setup(name='hdku',
      python_requires='>=3.6',
      version=0.1,
      url='https://github.com/haven-jeon/HDKU',
      license='GPL-3',
      author='Heewon Jeon',
      author_email='madjakarta@gmail.com',
      description='Python package for Hangul Dubeolsik Keystroke Utils',
      packages=['hdku', ],
      long_description=open('README.md', encoding='utf-8').read(),
      zip_safe=False,
      include_package_data=True,
      install_requires=[]
      )
