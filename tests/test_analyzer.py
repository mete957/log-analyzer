from click.testing import CliRunner
from log_analyzer.analyzer import main
import pytest
import json
import csv
from io import StringIO

@pytest.fixture
def sample_log(tmp_path):
    log_content = ("INFO Başlatıldı\n"
                   "ERROR Hata meydana geldi\n"
                   "WARNING Dikkat edilmeli\n"
                   "INFO İkinci info kaydı\n")
    log_file = tmp_path / "test.log"
    log_file.write_text(log_content, encoding='utf-8')
    return str(log_file)


def run_cli(args):
    runner = CliRunner()
    return runner.invoke(main, args)


def test_single_level_filter(sample_log):
    result = run_cli([sample_log, '--level', 'ERROR'])
    assert result.exit_code == 0
    assert 'Hata meydana geldi' in result.output
    assert 'Başlatıldı' not in result.output


def test_multi_level_filter(sample_log):
    result = run_cli([sample_log, '--level', 'INFO,WARNING'])
    assert result.exit_code == 0
    # INFO lines
    assert 'Başlatıldı' in result.output
    assert 'İkinci info kaydı' in result.output
    # WARNING line
    assert 'Dikkat edilmeli' in result.output
    # ERROR line excluded
    assert 'Hata meydana geldi' not in result.output


def test_pattern_filter(sample_log):
    # Filter lines containing 'ikinci' (case-insensitive)
    result = run_cli([sample_log, '--pattern', '(?i)ikinci'])
    assert result.exit_code == 0
    assert 'İkinci info kaydı' in result.output
    assert 'Başlatıldı' not in result.output


def test_stats_text_output(sample_log):
    result = run_cli([sample_log, '--level', 'INFO,ERROR', '--stats'])
    assert result.exit_code == 0
    assert 'Summary Statistics:' in result.output
    # Expect 3 lines (2 INFO + 1 ERROR)
    assert '- INFO: 2 lines' in result.output
    assert '- ERROR: 1 lines' in result.output


def test_stats_json_output(sample_log):
    result = run_cli([sample_log, '--level', 'ERROR,WARNING', '--stats', '--output-format', 'json'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    levels = {item['level']: item for item in data['statistics']}
    assert levels['ERROR']['count'] == 1
    assert levels['WARNING']['count'] == 1


def test_stats_csv_output(sample_log):
    result = run_cli([sample_log, '--level', 'INFO,WARNING', '--stats', '--output-format', 'csv'])
    assert result.exit_code == 0
    # Parse CSV from output
    csv_reader = csv.DictReader(StringIO(result.output))
    rows = list(csv_reader)
    # Convert counts to int
    counts = {row['level']: int(row['count']) for row in rows}
    assert counts['INFO'] == 2
    assert counts['WARNING'] == 1
