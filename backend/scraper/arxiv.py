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

    def fetch_daily_papers(self, days_back: int = 7) -> List[Paper]:
        """获取最近几天的论文"""
        print(f"Fetching papers for the last {days_back} days...")
        papers = []
        
        # 构建搜索查询
        query = ' OR '.join(f'cat:{topic}' for topic in TOPICS_OF_INTEREST)
        print(f"Search query: {query}")
        
        search = arxiv.Search(
            query=query,
            max_results=ARXIV_RESULTS_PER_PAGE,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        try:
            print("Querying arXiv API...")
            results = list(self.client.results(search))
            print(f"Retrieved {len(results)} results from arXiv API")
            
            if not results:
                print("No results found from arXiv API")
                return papers
                
            # 使用最新论文的日期作为基准
            latest_date = results[0].published.date()
            earliest_date = latest_date - timedelta(days=days_back)
            print(f"Latest paper date: {latest_date}")
            print(f"Date range: {earliest_date} to {latest_date}")
            
            # 解析论文
            skipped_count = 0
            for result in results:
                try:
                    pub_date = result.published.date()
                    print(f"Processing paper ID: {result.get_short_id()}, "
                          f"Published: {pub_date}")
                    
                    if pub_date >= earliest_date:
                        paper = self._parse_paper(result)
                        papers.append(paper)
                        print(f"Added paper: {paper.title[:50]}... "
                              f"[{paper.categories}]")
                        skipped_count = 0  # 重置跳过计数
                    else:
                        skipped_count += 1
                        if skipped_count > 50:  # 如果连续跳过50篇论文，则退出
                            print("Too many old papers, stopping...")
                            break
                except Exception as e:
                    print(f"Error parsing paper {result.get_short_id()}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching papers: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"\nTotal papers found: {len(papers)}")
        return papers