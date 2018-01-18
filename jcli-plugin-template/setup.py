from setuptools import setup, find_packages

setup(
    name="jcli_plugin_template",
    version="1.0",
    author="JSlabaugh",
    author_email="jeffrey.slabaugh@gmail.com",
    description="Template for quickly building out a plugin CLI",
    license="Proprietary",
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    package_data={'jcli_plugin_template': ['conf/template.conf']},
    entry_points={
        'jcli.plugins': "example=jcli_plugin_template.plugin.template:Example"
    }
)
