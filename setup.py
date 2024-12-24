import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_diff_pdf2",
    version="1.0.0",
    author="lwinhong",
    url='xxx',
    author_email="xxx",
    description="xxx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(
        where="src",
        include=["py_diff_pdf2", "py_diff_pdf2.libs.*", "py_diff_pdf2.*"], ),
    python_requires=">=3.6",
    include_package_data=True
)
