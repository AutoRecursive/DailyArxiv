from ..scraper.arxiv import ArxivScraper
from ..database.db import Database
from ..config import DATABASE_PATH
from datetime import datetime, timedelta

def test_full_pipeline():
    # 初始化数据库和爬虫
    db = Database(DATABASE_PATH)
    scraper = ArxivScraper()
    
    # 清理旧数据
    deleted_count = db.cleanup_old_papers(days_to_keep=7)
    if deleted_count > 0:
        print(f"\n清理了 {deleted_count} 篇7天前的旧论文")
    
    # 获取最近7天的论文
    papers = scraper.fetch_daily_papers(days_back=7)
    
    # ... (保持其他测试代码不变) ...

if __name__ == "__main__":
    test_full_pipeline() 