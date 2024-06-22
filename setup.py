from setuptools import setup,find_packages
from typing import List

DASH_E_DOT="-e ."
def get_requirements(filepath:str)->List[str]:
    requirements=[]
    with open(filepath) as fileobj:
        requirements=fileobj.readlines()
        requirements=[req.replace("\n","")for req in requirements]

    if DASH_E_DOT in requirements:
        requirements.remove(DASH_E_DOT)
    
    return requirements

setup(
        name="mlproject",
        version="0.0.1",
        author="sudipta",
        author_email="sudipmaha123@gmail.com",
        packages=find_packages(),
        install_requires=get_requirements('requirements.txt')
)