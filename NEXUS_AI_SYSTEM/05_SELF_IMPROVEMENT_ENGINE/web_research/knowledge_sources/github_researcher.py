# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/web_research/knowledge_sources/github_researcher.py ---

import requests
import os
from typing import List, Dict, Optional, Any

class GitHubResearcher:
    """
    A client to search for code, repositories, and issues on GitHub using its API.

    This component enables the Self-Improvement Engine to find real-world code
    implementations, track popular libraries, and discover solutions to technical
    challenges.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, api_token: Optional[str] = None):
        """
        Initializes the GitHub researcher client.

        Args:
            api_token (Optional[str]): A GitHub API token to increase rate limits.
                                       If not provided, it attempts to use the
                                       GITHUB_API_TOKEN environment variable.
        """
        self.api_token = api_token or os.environ.get("GITHUB_API_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.api_token:
            self.headers["Authorization"] = f"token {self.api_token}"
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
        """
        Sends a GET request to a specified GitHub API endpoint.

        Args:
            endpoint (str): The API endpoint to query (e.g., '/search/repositories').
            params (Optional[Dict]): A dictionary of query parameters.

        Returns:
            Optional[Any]: The JSON response from the API, or None if the request fails.
        """
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", headers=self.headers, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during GitHub API request: {e}")
            return None

    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 10) -> Optional[List[Dict]]:
        """
        Searches for repositories on GitHub.

        Args:
            query (str): The search query.
            sort (str): The sort field. Can be 'stars', 'forks', or 'updated'.
            order (str): The sort order. Can be 'asc' or 'desc'.
            per_page (int): Number of results to return per page.

        Returns:
            Optional[List[Dict]]: A list of repository dictionaries, or None.
        """
        print(f"\n--- Searching GitHub repositories for: '{query}' ---")
        params = {'q': query, 'sort': sort, 'order': order, 'per_page': per_page}
        data = self._make_request("/search/repositories", params=params)
        return data['items'] if data else None

    def search_code(self, query: str, language: str = None, per_page: int = 10) -> Optional[List[Dict]]:
        """
        Searches for code snippets within repositories.

        Args:
            query (str): The code to search for.
            language (str, optional): The programming language to filter by.
            per_page (int): Number of results to return.

        Returns:
            Optional[List[Dict]]: A list of code search result items, or None.
        """
        print(f"\n--- Searching GitHub code for: '{query}' ---")
        if language:
            query += f" language:{language}"
        params = {'q': query, 'per_page': per_page}
        data = self._make_request("/search/code", params=params)
        return data['items'] if data else None

    def get_repo_details(self, repo_full_name: str) -> Optional[Dict]:
        """
        Retrieves detailed information for a specific repository.

        Args:
            repo_full_name (str): The full name of the repository (e.g., 'facebook/react').

        Returns:
            Optional[Dict]: A dictionary containing repository details, or None.
        """
        print(f"\n--- Getting details for repository: {repo_full_name} ---")
        return self._make_request(f"/repos/{repo_full_name}")

if __name__ == '__main__':
    print("--- Running GitHub Researcher Example ---")
    
    # For more extensive use, set a GITHUB_API_TOKEN environment variable
    researcher = GitHubResearcher()

    if not researcher.api_token:
        print("\nWarning: GITHUB_API_TOKEN not set. Using anonymous access, which has a lower rate limit.")

    # 1. Search for popular repositories related to "flash-attention"
    repo_query = "flash-attention"
    repos = researcher.search_repositories(repo_query, sort='stars', per_page=5)
    if repos:
        print(f"\n--- Top 5 Repositories for '{repo_query}' ---")
        for repo in repos:
            print(f"- {repo['full_name']}: {repo['stargazers_count']} stars - {repo['description']}")
    else:
        print(f"Could not fetch repository search results.")

    # 2. Search for code implementations of "FlashAttention" in Python
    code_query = 'class FlashAttention'
    code_results = researcher.search_code(code_query, language='python', per_page=5)
    if code_results:
        print(f"\n--- Top 5 Code Snippets for '{code_query}' (Python) ---")
        for item in code_results:
            print(f"- Repository: {item['repository']['full_name']}")
            print(f"  File: {item['path']}")
            print(f"  URL: {item['html_url']}")
    else:
        print(f"Could not fetch code search results.")

    # 3. Get details for a specific repository
    repo_name = 'Dao-AILab/flash-attention'
    repo_details = researcher.get_repo_details(repo_name)
    if repo_details:
        print(f"\n--- Details for {repo_name} ---")
        print(f"Description: {repo_details['description']}")
        print(f"Stars: {repo_details['stargazers_count']}")
        print(f"Forks: {repo_details['forks_count']}")
        print(f"Homepage: {repo_details['homepage']}")
    else:
        print(f"Could not fetch details for repository {repo_name}.")
