import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
	'console_scripts': [
	],
}

TESTS_REQUIRE = [
	'nose',
	'nose-timer',
	'nose-pudb',
	'nose-progressive',
	'nose2[coverage_plugin]',
	'pyhamcrest',
	'nti.nose_traceback_info',
	'nti.testing'
]

setup(
	name='nti.mimetype',
	version=VERSION,
	author='Jason Madden',
	author_email='jason@nextthought.com',
	description="NTI MimeType",
	long_description=codecs.open('README.rst', encoding='utf-8').read(),
	license='Proprietary',
	keywords='MimeTypes',
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: Implementation :: CPython'
	],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
	tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
		'dolmen.builtins',
		'zope.component',
		'zope.deferredimport',
		'zope.interface',
		'zope.mimetype',
		'zope.security',
		'nti.common',
		'nti.coremetadata',
		'nti.externalization'
	],
	extras_require={
		'test': TESTS_REQUIRE,
	},
	entry_points=entry_points
)
