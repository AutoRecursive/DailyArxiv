import sys
import os

# 添加项目根目录到 Python 路径
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

from backend.scraper.arxiv import ArxivScraper

def test_fetch():
    scraper = ArxivScraper()
    # 设置获取最近7天的论文
    papers = scraper.fetch_daily_papers(days_back=7)
    
    print("\n=== 测试结果汇总 ===")
    print(f"总共获取到 {len(papers)} 篇论文")
    if papers:
        print("\n示例论文：")
        paper = papers[0]
        print(f"标题: {paper.title}")
        print(f"作者: {paper.authors}")
        print(f"分类: {paper.categories}")
        print(f"发布日期: {paper.published_date}")
        print(f"PDF链接: {paper.pdf_url}")

if __name__ == "__main__":
    test_fetch() 