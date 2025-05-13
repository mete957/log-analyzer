import click

@click.command()
@click.argument('logfile', type=click.Path(exists=True))
@click.option('--level', '-l', default='INFO', help='Log seviyesi (INFO, WARNING, ERROR)')
def main(logfile, level):
    """
    Verilen log dosyasını analiz eder ve belirtilen seviyedeki logları gösterir.
    """
    click.echo(f"Analiz edilen log dosyası: {logfile}")
    click.echo(f"Filtreleme seviyesi: {level}")

    with open(logfile, 'r') as file:
        for line in file:
            if level in line:
                click.echo(line.strip())

if __name__ == '__main__':
    main()
