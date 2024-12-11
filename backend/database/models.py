from datetime import datetime
from dataclasses import dataclass

@dataclass
class Paper:
    id: str                     # arXiv ID
    title: str                  # 论文标题
    authors: str                # 作者列表
    abstract: str               # 摘要
    categories: str             # 分类类别
    published_date: datetime    # 发布日期
    updated_date: datetime      # 更新日期
    pdf_url: str               # PDF 下载链接 