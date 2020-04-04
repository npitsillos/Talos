from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

kwargs = {
    "include_package_data": True,
    "install_requires": load_requirements("requirements.txt")
}

setup(**kwargs)