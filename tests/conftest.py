import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

src_path = str(Path(__file__).parent.parent / 'src')
sys.path.insert(0, src_path)

os.environ['BOT_TOKEN'] = '123:test_token'


sys.modules['database'] = MagicMock()
sys.modules['database'].Database = MagicMock()
