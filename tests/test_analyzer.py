from click.testing import CliRunner
from log_analyzer.analyzer import main
import pytest
import os

@pytest.fixture
def sample_log(tmp_path):
    log_content = """INFO Başlatıldı
ERROR Hata meydana geldi
WARNING Dikkat edilmesi gereken durum"""
    log_file = tmp_path / "test.log"
    log_file.write_text(log_content)
    return str(log_file)

def test_log_analyzer_info(sample_log):
    runner = CliRunner()
    result = runner.invoke(main, [sample_log, '--level', 'INFO'])
    assert result.exit_code == 0
    assert 'Başlatıldı' in result.output

def test_log_analyzer_error(sample_log):
    runner = CliRunner()
    result = runner.invoke(main, [sample_log, '--level', 'ERROR'])
    assert result.exit_code == 0
    assert 'Hata meydana geldi' in result.output
