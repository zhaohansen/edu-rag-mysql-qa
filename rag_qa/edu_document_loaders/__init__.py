import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)
# 导入配置
from base.config import Config

# 条件导入各个文档加载器，允许在缺少依赖时继续运行
try:
    from .edu_docloader import *
except ImportError:
    pass

try:
    from .edu_pptloader import *
except ImportError:
    pass

try:
    from .edu_imgloader import *
except ImportError:
    pass

try:
    from .edu_pdfloader import *
except ImportError:
    pass
