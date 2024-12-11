from ..scraper.arxiv import ArxivScraper

def test_scraper():
    scraper = ArxivScraper()
    papers = scraper.fetch_daily_papers(days_back=3)
    
    print(f"\n总共获取到 {len(papers)} 篇近3天的论文\n")
    
    # 打印前5篇论文的基本信息
    for i, paper in enumerate(papers[:5], 1):
        print(f"论文 {i}:")
        print(f"标题: {paper.title}")
        print(f"作者: {paper.authors}")
        print(f"分类: {paper.categories}")
        print(f"发布时间: {paper.published_date}")
        print(f"PDF链接: {paper.pdf_url}")
        print("-" * 80)

if __name__ == "__main__":
    test_scraper() 