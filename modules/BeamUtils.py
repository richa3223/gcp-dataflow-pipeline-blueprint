# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Apache Beam utilities
"""

__all__ = [
  "CsvFileSource",
]

from apache_beam.io.filebasedsource import FileBasedSource
from io import TextIOWrapper
from csv import DictReader

class CsvFileSource(FileBasedSource):
  """Custom source parsing CSV files"""

  def read_records(self, file_name, range_tracker):
    """Reads a CSV file returning each row as a dictionary"""
    self._file = self.open_file(file_name)
    with TextIOWrapper(self._file, encoding='utf-8') as text_file:
      reader = DictReader(text_file)
      for row in reader:
        yield row

# fmt: on