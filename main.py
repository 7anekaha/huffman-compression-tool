import click
from huffman import HuffmanCompression


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True),
    help="Input file to compress.",
)
@click.option(
    "--output",
    "output_file",
    required=False,
    default=None,
    type=click.Path(),
    help="Output file for compressed data.",
)
def compress(input_file, output_file):
    """Compress a file using Huffman algorithm"""
    click.echo(f"Compressing {input_file}")
    HuffmanCompression.encode(input_file, output_file)
    click.echo("Compression finished")


@cli.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True),
    help="Input file to decompress.",
)
@click.option(
    "--output",
    "output_file",
    required=False,
    default=None,
    type=click.Path(),
    help="Output file for decompressed data.",
)
def decompress(input_file, output_file):
    """Decompress a file using Huffman algorithm"""
    click.echo(f"Decompressing {input_file}")
    HuffmanCompression.decode(input_file, output_file)
    click.echo("Decompression finished")


if __name__ == "__main__":
    cli()
