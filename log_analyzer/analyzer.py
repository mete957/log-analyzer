import sys
import click
import re
import json
import csv
from collections import Counter

# Color mapping for log levels
LEVEL_COLORS = {
    'ERROR': 'red',
    'WARNING': 'yellow',
    'INFO': 'green'
}

@click.command()
@click.argument('logfile', type=click.Path())
@click.option('--level', '-l', default=None,
              help='Comma-separated log levels to include (e.g., INFO,ERROR)')
@click.option('--pattern', '-p', default=None,
              help='Regex pattern to filter lines')
@click.option('--stats', is_flag=True,
              help='Display summary statistics of matched lines')
@click.option('--output-format', type=click.Choice(['text', 'json', 'csv']), default='text',
              help='Output format for statistics')
def main(logfile, level, pattern, stats, output_format):
    """
    Performant log analyzer with streaming and minimal memory usage.

    - --level: Virgülle ayrılmış seviyelere göre filtreleme.
    - --pattern: Regex deseni ile filtreleme.
    - --stats: Özet istatistik (metin/json/csv).
    """
    # File access error handling
    try:
        f = open(logfile, 'r', encoding='utf-8')
    except FileNotFoundError:
        click.secho(f"Error: Dosya bulunamadı: {logfile}", fg='red', err=True)
        sys.exit(1)
    except Exception as e:
        click.secho(f"Error: {e}", fg='red', err=True)
        sys.exit(1)

    levels = [lvl.strip() for lvl in level.split(',')] if level else None
    regex = re.compile(pattern) if pattern else None
    counts = Counter()
    pure_stats_mode = stats and output_format in ('json', 'csv')

    # Stream processing
    with f:
        for raw in f:
            line = raw.rstrip('\n')
            # Filtering
            if levels and not any(lvl in line for lvl in levels):
                continue
            if regex and not regex.search(line):
                continue
            # Count for stats
            if levels:
                for lvl in levels:
                    if lvl in line:
                        counts[lvl] += 1
                        break
            else:
                parts = line.split()
                if parts and parts[0].isupper():
                    counts[parts[0]] += 1
            # If not pure stats JSON/CSV, print line immediately
            if not pure_stats_mode:
                color = next((LEVEL_COLORS.get(lvl) for lvl in LEVEL_COLORS if lvl in line), None)
                if color:
                    click.echo(click.style(line, fg=color))
                else:
                    click.echo(line)

    # Output stats
    if stats:
        total = sum(counts.values())
        stats_data = [{'level': lvl, 'count': cnt, 'percentage': round((cnt / total * 100) if total > 0 else 0, 2)}
                      for lvl, cnt in counts.items()]

        if output_format == 'json':
            click.echo(json.dumps({'statistics': stats_data}, ensure_ascii=False, indent=2))
            return
        elif output_format == 'csv':
            writer = csv.DictWriter(
                f=click.get_text_stream('stdout'),
                fieldnames=['level', 'count', 'percentage']
            )
            writer.writeheader()
            writer.writerows(stats_data)
            return
        else:
            click.secho('\nSummary Statistics:', bold=True)
            for item in stats_data:
                line = f"- {item['level']}: {item['count']} lines ({item['percentage']}%)"
                color = LEVEL_COLORS.get(item['level'])
                if color:
                    click.echo(click.style(line, fg=color))
                else:
                    click.echo(line)

if __name__ == '__main__':
    main()
