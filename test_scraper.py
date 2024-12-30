import sys
import os
from datetime import datetime

# 添加项目根目录到 Python 路径
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

from backend.scraper.arxiv import ArxivScraper
from backend.database.db import Database
from backend.config import DATABASE_PATH, TOPICS_OF_INTEREST

def test_update():
    print("\n=== 开始测试 ArXiv 更新功能 ===")
    print(f"当前时间: {datetime.now()}")
    print(f"监控的主题: {', '.join(TOPICS_OF_INTEREST)}")
    
    # 初始化爬虫
    scraper = ArxivScraper()
    
    # 获取最近7天的论文
    print("\n1. 获取论文...")
    papers = scraper.fetch_daily_papers(days_back=7)
    
    print(f"\n获取到 {len(papers)} 篇论文")
    
    if papers:
        print("\n2. 论文示例:")
        for i, paper in enumerate(papers[:3], 1):  # 显示前3篇论文
            print(f"\n论文 {i}:")
            print(f"ID: {paper.id}")
            print(f"标题: {paper.title}")
            print(f"作者: {paper.authors}")
            print(f"分类: {paper.categories}")
            print(f"发布日期: {paper.published_date}")
            print(f"PDF: {paper.pdf_url}")
            print("-" * 80)
    else:
        print("\n警告: 没有获取到任何论文!")
        
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_update() 