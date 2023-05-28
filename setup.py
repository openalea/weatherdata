# -*- python -*-
#
#       Copyright INRIA - CIRAD - INRA
#
#       File author(s):
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://github.com/openalea/weatherdata
#
# ==============================================================================
"""
"""
# ==============================================================================
from setuptools import setup, find_packages
# ==============================================================================

pkg_root_dir = 'src'
packages = [pkg for pkg in find_packages(pkg_root_dir)]
top_pkgs = [pkg for pkg in packages if len(pkg.split('.')) <= 2]
package_dir = dict([('', pkg_root_dir)] +
                   [(pkg, pkg_root_dir + "/" + pkg.replace('.', '/'))
                    for pkg in top_pkgs])

_version = {}
with open("src/weatherdata/version.py") as fp:
    exec(fp.read(), _version)
version = _version['version']

description = 'Python data structure for handling weather data in OpenAlea.'
long_description = 'Python data structure for handling weather data in OpenAlea.'

setup(
    name="weatherdata",
    version=version,
    description=description,
    long_description=long_description,

    author="* Christian Fournier\n"
           "* Marc Labadie\n"
           "* Christophe Pradal\n",

    maintainer="",
    maintainer_email="",

    url="",
    license="Cecill-C",
    keywords='openalea, DSS, weather',

    # package installation
    packages=packages,
    package_dir=package_dir,
    zip_safe=False,

    # See MANIFEST.in
    include_package_data=True,

    entry_points = {
       "wralea": ["weatherdata = weatherdata.wralea",
                  "ipmdecisions = weatherdata.ipmwralea"]},    

    )
