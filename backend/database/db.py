import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional
from .models import Paper

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    abstract TEXT NOT NULL,
                    categories TEXT NOT NULL,
                    published_date TIMESTAMP NOT NULL,
                    updated_date TIMESTAMP NOT NULL,
                    pdf_url TEXT NOT NULL
                )
            """)

    def insert_paper(self, paper: Paper) -> bool:
        """插入新论文"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO papers 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    paper.id,
                    paper.title,
                    paper.authors,
                    paper.abstract,
                    paper.categories,
                    paper.published_date,
                    paper.updated_date,
                    paper.pdf_url
                ))
            return True
        except Exception as e:
            print(f"Error inserting paper: {e}")
            return False

    def get_papers_by_date(self, date: datetime) -> List[Paper]:
        """获取指定日期发布的论文"""
        print(f"Fetching papers for date: {date.date()}")  # 添加日志
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM papers 
                WHERE DATE(published_date) = DATE(?)
                ORDER BY published_date DESC
            """, (date.date(),))
            
            rows = cursor.fetchall()
            print(f"Found {len(rows)} papers in database")  # 添加日志
            papers = []
            for row in rows:
                data = dict(row)
                # 确保日期是字符串格式
                if data['published_date']:
                    data['published_date'] = str(data['published_date'])
                if data['updated_date']:
                    data['updated_date'] = str(data['updated_date'])
                papers.append(Paper(**data))
            return papers

    def cleanup_old_papers(self, days_to_keep: int = 7) -> int:
        """删除指定天数之前的论文
        
        Args:
            days_to_keep: 保留最近几天的论文，默认7天
            
        Returns:
            删除的论文数量
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    DELETE FROM papers 
                    WHERE DATE(published_date) < DATE(?)
                """, (cutoff_date,))
                return cursor.rowcount
        except Exception as e:
            print(f"Error cleaning up old papers: {e}")
            return 0