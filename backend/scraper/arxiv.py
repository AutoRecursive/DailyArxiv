import arxiv
from datetime import datetime, timedelta
from typing import List
from backend.database.models import Paper
from backend.config import TOPICS_OF_INTEREST, ARXIV_RESULTS_PER_PAGE

class ArxivScraper:
    def __init__(self):
        self.client = arxiv.Client()

    def _parse_paper(self, result) -> Paper:
        """解析单个论文"""
        return Paper(
            id=result.get_short_id(),
            title=result.title,
            authors=', '.join(author.name for author in result.authors),
            abstract=result.summary,
            categories=', '.join(result.categories),
            published_date=result.published,
            updated_date=result.updated,
            pdf_url=result.pdf_url
        )

    def fetch_daily_papers(self, days_back: int = 3) -> List[Paper]:
        """获取最近几天的论文"""
        print(f"Fetching papers for the last {days_back} days...")
        papers = []
        
        # 构建搜索查询
        query = ' OR '.join(f'cat:{topic}' for topic in TOPICS_OF_INTEREST)
        print(f"Search query: {query}")  # 添加查询日志
        
        search = arxiv.Search(
            query=query,
            max_results=ARXIV_RESULTS_PER_PAGE,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        try:
            print("Querying arXiv API...")
            results = list(self.client.results(search))  # 转换为列表以便计数
            print(f"Retrieved {len(results)} results from arXiv API")  # 添加结果数量日志
            
            # 获取日期范围
            today = datetime.now()
            earliest_date = today - timedelta(days=days_back)
            print(f"Date range: {earliest_date.date()} to {today.date()}")  # 添加日期范围日志
            
            # 解析论文
            for result in results:
                try:
                    print(f"Processing paper ID: {result.get_short_id()}, "
                          f"Published: {result.published.date()}")  # 添加处理日志
                    # 获取最近几天的论文
                    if result.published.date() >= earliest_date.date():
                        paper = self._parse_paper(result)
                        papers.append(paper)
                        print(f"Added paper: {paper.title[:50]}... "
                              f"[{paper.categories}]")  # 添加更详细的论文信息
                    else:
                        print(f"Skipping older paper: {result.get_short_id()}")
                        break
                except Exception as e:
                    print(f"Error parsing paper {result.get_short_id()}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching papers: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"Total papers found: {len(papers)}")
        return papers