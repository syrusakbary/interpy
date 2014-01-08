import os, sys

try:
    from setuptools import setup
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install


def _post_install(install_lib):
    import shutil
    shutil.copy('interpy.pth', install_lib)

class install(_install):
    def run(self):
        self.path_file = 'interpy'
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")

version = "1.1"

setup(
    cmdclass={'install': install},
    name="interpy",
    version=version,
    download_url='git@github.com:syrusakbary/interpy.git',
    packages = ["interpy", "interpy.codec"],
    author='Syrus Akbary',
    author_email='me@syrusakbary.com',
    url="http://github.com/syrusakbary/interpy",
    license='MIT',
    description="Interpy extends Python to support Ruby like string interpolation #{}.",
    long_description=open('README.rst').read(),
    keywords='python string interpolation interpolate ruby codec',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
