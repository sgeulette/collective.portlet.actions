from setuptools import setup, find_packages
import os

setup(
    name='collective.portlet.actions',
    version='1.2.4.dev0',
    description="A portlet that provides the links of an action category",
    long_description=(open("README.rst").read().strip() + "\n\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read().strip()),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone portlet',
    author='Gilles Lenfant',
    author_email='gilles.lenfant@alterway.fr',
    url='https://github.com/collective/collective-portlet-actions',
    download_url='https://pypi.org/project/collective-portlet-actions',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.portlet'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'Acquisition',
        'Products.CMFCore',
        'Zope2',
        'plone.app.portlets',
        'plone.memoize',
    ],
    extras_require={'test': ['Products.PloneTestCase']},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """
)
