from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from backend.database.db import Database
from backend.scraper.arxiv import ArxivScraper
from backend.config import DATABASE_PATH
from backend.database.models import Paper

app = FastAPI(title="ArXiv Paper Service")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库和爬虫
db = Database(DATABASE_PATH)
scraper = ArxivScraper()

def update_papers():
    """定时任务：更新论文数据并清理旧数据"""
    try:
        # 清理旧数据
        deleted_count = db.cleanup_old_papers(days_to_keep=7)
        if deleted_count > 0:
            print(f"Cleaned up {deleted_count} old papers")

        # 获取新论文
        papers = scraper.fetch_daily_papers()
        success_count = 0
        for paper in papers:
            if db.insert_paper(paper):
                success_count += 1
        print(f"Successfully fetched and stored {success_count} papers")
    except Exception as e:
        print(f"Error in update task: {e}")

# 设置定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(update_papers, 'interval', hours=6)
scheduler.start()

@app.get("/papers/recent")
async def get_recent_papers(
    days: int = Query(1, ge=1, le=7, description="获取最近几天的论文"),
    category: Optional[str] = Query(None, description="按分类筛选"),
    limit: int = Query(50, ge=1, le=100, description="返回的论文数量限制")
):
    """获取最近的论文"""
    try:
        print(f"Fetching papers with params: days={days}, category={category}, limit={limit}")  # 添加日志
        papers = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            day_papers = db.get_papers_by_date(date)
            print(f"Found {len(day_papers)} papers for date {date.date()}")  # 添加日志
            papers.extend(day_papers)
        
        # 按分类筛选
        if category:
            papers = [p for p in papers if category in p.categories]
            print(f"After category filter: {len(papers)} papers")  # 添加日志
        
        # 按发布时间排序并限制数量
        papers.sort(key=lambda x: x.published_date, reverse=True)
        papers = papers[:limit]
        
        return [{
            'id': p.id,
            'title': p.title,
            'authors': p.authors,
            'abstract': p.abstract,
            'categories': p.categories,
            'published_date': p.published_date if isinstance(p.published_date, str) else p.published_date.isoformat() if p.published_date else None,
            'updated_date': p.updated_date if isinstance(p.updated_date, str) else p.updated_date.isoformat() if p.updated_date else None,
            'pdf_url': p.pdf_url
        } for p in papers]

    except Exception as e:
        print(f"Error processing request: {e}")  # 添加错误日志
        import traceback
        traceback.print_exc()  # 打印完整错误堆栈
        return {"error": "Internal server error", "message": str(e)}

@app.get("/papers/categories")
async def get_categories():
    """获取所有可用的论文分类"""
    try:
        papers = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            papers.extend(db.get_papers_by_date(date))
        
        category_stats = {}
        for paper in papers:
            for category in paper.categories.split(', '):
                category_stats[category] = category_stats.get(category, 0) + 1
        
        return sorted(
            [{"category": k, "count": v} for k, v in category_stats.items()],
            key=lambda x: x["count"],
            reverse=True
        )
    except Exception as e:
        print(f"Error processing categories request: {e}")
        return {"error": "Internal server error", "message": str(e)}

@app.get("/papers/stats")
async def get_stats():
    """获取论文统计信息"""
    try:
        papers = []
        daily_stats = {}
        
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            day_papers = db.get_papers_by_date(date)
            daily_stats[date.date().isoformat()] = len(day_papers)
            papers.extend(day_papers)
        
        return {
            "total_papers": len(papers),
            "daily_stats": daily_stats,
        }
    except Exception as e:
        print(f"Error processing stats request: {e}")
        return {"error": "Internal server error", "message": str(e)}

@app.post("/papers/update")
async def trigger_update():
    """手动触发论文更新"""
    try:
        # 清理旧数据
        deleted_count = db.cleanup_old_papers(days_to_keep=7)
        
        # 获取新论文
        papers = scraper.fetch_daily_papers()
        success_count = 0
        for paper in papers:
            if db.insert_paper(paper):
                success_count += 1
        
        return {
            "status": "success",
            "deleted_papers": deleted_count,
            "new_papers": success_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error in manual update: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# 启动时运行一次更新
update_papers()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, reload=True) 