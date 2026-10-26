import logging
from base.config import Config
from pathlib import Path
import tempfile

project_root = Path(__file__).resolve().parent.parent
log_file = project_root / Config.log_file
log_file.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger('mysql_query')
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Desktop-protected folders can reject writes even when the project is
    # readable. Keep logging from preventing the application from starting.
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
    except (PermissionError, OSError):
        fallback_dir = Path(tempfile.gettempdir()) / "mysql_query"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(fallback_dir / "app.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
