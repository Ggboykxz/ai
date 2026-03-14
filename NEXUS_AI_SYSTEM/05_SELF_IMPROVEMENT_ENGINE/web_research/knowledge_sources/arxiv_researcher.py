# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/web_research/knowledge_sources/arxiv_researcher.py ---

import arxiv
from typing import List, Dict, Optional

class ArxivResearcher:
    """
    A client to search for and retrieve academic papers from arXiv.

    This component is crucial for the Self-Improvement Engine to stay up-to-date
    with the latest scientific advancements in machine learning, mathematics,
    and computer science.
    """

    def __init__(self, max_results: int = 10):
        """
        Initializes the Arxiv researcher client.

        Args:
            max_results (int): The default maximum number of results to return for a search.
        """
        self.client = arxiv.Client()
        self.max_results = max_results

    def search_papers(self, query: str, sort_by=arxiv.SortCriterion.Relevance) -> List[Dict]:
        """
        Searches for papers on arXiv based on a query.

        Args:
            query (str): The search query (e.g., 'transformer architecture', 'mixture of experts').
            sort_by: The criterion for sorting results. 
                     Options: Relevance, LastUpdatedDate, SubmittedDate.

        Returns:
            List[Dict]: A list of dictionaries, where each dictionary contains 
                        metadata for a found paper.
        """
        print(f"\n--- Searching arXiv for query: '{query}' ---")
        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=sort_by
        )

        results = list(self.client.results(search))
        print(f"Found {len(results)} papers.")

        return [self._format_paper(paper) for paper in results]

    def get_paper_by_id(self, paper_id: str) -> Optional[Dict]:
        """
        Retrieves a single paper by its arXiv ID (e.g., '1706.03762').

        Args:
            paper_id (str): The unique identifier of the paper on arXiv.

        Returns:
            Optional[Dict]: A dictionary with the paper's metadata, or None if not found.
        """
        print(f"--- Fetching paper by ID: {paper_id} ---")
        try:
            search = arxiv.Search(id_list=[paper_id])
            paper = next(self.client.results(search))
            return self.format_paper(paper)
        except StopIteration:
            print(f"Paper with ID '{paper_id}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while fetching paper {paper_id}: {e}")
            return None

    def _format_paper(self, paper: arxiv.Result) -> Dict:
        """
        Formats an arxiv.Result object into a structured dictionary.
        """
        return {
            'id': paper.get_short_id(),
            'title': paper.title,
            'summary': paper.summary,
            'authors': [str(author) for author in paper.authors],
            'categories': paper.categories,
            'published_date': paper.published.isoformat(),
            'updated_date': paper.updated.isoformat(),
            'pdf_url': paper.pdf_url,
            'doi': paper.doi,
        }

    def get_summary(self, paper_result: Dict) -> str:
        """
        Returns a concise, formatted summary of a paper dictionary.
        """
        summary = f"Title: {paper_result['title']}\n"
        summary += f"Authors: {', '.join(paper_result['authors'])}\n"
        summary += f"Published: {paper_result['published_date']}\n"
        summary += f"URL: https://arxiv.org/abs/{paper_result['id']}\n\n"
        summary += f"Abstract:\n{paper_result['summary']}"
        return summary

if __name__ == '__main__':
    # Example usage: Find recent papers about Mixture of Experts.
    print("--- Running Arxiv Researcher Example ---")
    researcher = ArxivResearcher(max_results=5)

    # 1. Search for papers
    search_query = "Mixture of Experts for Language Models"
    try:
        papers = researcher.search_papers(query=search_query, sort_by=arxiv.SortCriterion.LastUpdatedDate)

        if papers:
            print(f"\n--- Top {len(papers)} Recent Papers on '{search_query}' ---")
            for i, paper in enumerate(papers):
                print(f"\n--- Result {i+1} ---")
                print(researcher.get_summary(paper))
        else:
            print("No papers found for the query.")

        # 2. Fetch a specific, well-known paper
        attention_paper_id = "1706.03762" # "Attention Is All You Need"
        print(f"\n--- Fetching a Classic Paper by ID: {attention_paper_id} ---")
        attention_paper = researcher.get_paper_by_id(attention_paper_id)
        if attention_paper:
            print(researcher.get_summary(attention_paper))

    except Exception as e:
        print(f"An error occurred during the arXiv API call: {e}")
        print("This might be due to network issues or rate limiting.")
