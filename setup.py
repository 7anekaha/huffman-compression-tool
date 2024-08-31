from setuptools import setup

setup(
    name="huffmanCompression",
    version="0.1",
    py_modules=["huffman2", "tree", "main"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        huff-zip=main:cli
    """,
    author="7anekaha",
    python_requires=">=3.9",
)
