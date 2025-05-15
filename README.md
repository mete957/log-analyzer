# Log Analyzer

**Log Analyzer**, terminal üzerinden log dosyalarınızı hızlıca filtreleyip istatistik çıkarabileceğiniz hafif bir CLI aracıdır.

---

## Özellikler

* **Seviye Bazlı Filtreleme** (`--level INFO,WARNING,ERROR`)
* **Regex Deseniyle Filtreleme** (`--pattern "Desen"`)
* **Özet İstatistik** (`--stats`)
* **Çıktı Formatları**: `text` (varsayılan), `json`, `csv` (`--output-format`)
* **Renkli Konsol Çıktısı** (INFO=yeşil, WARNING=sarı, ERROR=kırmızı)
* **Bellek Dostu**: Dosyayı satır satır işleyerek büyük log’larda performans sunar

---

## Kurulum

1. Depoyu klonlayın:

   ```bash
   git clone https://github.com/mete957/log-analyzer.git
   cd log-analyzer
   ```
2. Sanal ortam oluşturup etkinleştirin:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: .\venv\Scripts\activate
   ```
3. Gerekli paketleri yükleyin:

   ```bash
   pip install --upgrade pip setuptools wheel click
   pip install -e .
   ```

---

## ⚙️ Kullanım

Genel komut:

```bash
log-analyzer <logfile> [options]
```

### Ana Seçenekler

* `-l, --level LEVELS`
  Virgülle ayrılmış log seviyeleri (örn. `INFO,ERROR`).

* `-p, --pattern PATTERN`
  Regex deseni (örn. `"(?i)timeout"`).

* `--stats`
  Seçilen satırlar için özet istatistikleri gösterir.

* `--output-format {text,json,csv}`
  İstatistik çıktısı formatı (varsayılan `text`).

### Örnekler

1. **Sadece ERROR satırlarını göster**

   ```bash
   log-analyzer example.log --level ERROR
   ```

2. **INFO ve WARNING satırlarını gösterip istatistikle**

   ```bash
   log-analyzer example.log -l INFO,WARNING --stats
   ```

3. **JSON formatında sadece istatistik**

   ```bash
   log-analyzer example.log -l ERROR,WARNING --stats --output-format json
   ```

4. **Disk içeriği geçen satırları regex ile filtrele**

   ```bash
   log-analyzer example.log -p "Disk"
   ```

---

## 📋 Yardım

Komut satırında `--help` yazarak tüm seçeneklere bakabilirsiniz:

```bash
log-analyzer --help
```

---

## 🛠️ Geliştirme

* Kodun modüler yapıda olması için `log_analyzer/` altındaki dosyaları inceleyebilirsiniz.
* Yeni filtreleme veya çıktı formatı eklemek için `analyzer.py` içinde ilgili bölümlere ekleme yapın.

