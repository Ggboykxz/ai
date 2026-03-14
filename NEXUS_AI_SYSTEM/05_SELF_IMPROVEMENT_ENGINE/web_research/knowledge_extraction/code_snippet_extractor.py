# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/web_research/knowledge_extraction/code_snippet_extractor.py ---

from bs4 import BeautifulSoup
import re
from typing import List, Dict

class CodeSnippetExtractor:
    """
    Extracts code snippets from HTML content, typically from documentation pages,
    blog posts, or GitHub file views.
    
    It uses BeautifulSoup to parse HTML and heuristics to find code blocks,
    such as text within `<pre><code>`, `<code>`, or markdown-style triple backticks.
    """

    def __init__(self, html_content: str):
        """
        Initializes the extractor with the HTML content of a webpage.

        Args:
            html_content (str): The raw HTML string.
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_snippets(self) -> List[Dict[str, str]]:
        """
        Finds and extracts all code snippets from the parsed HTML.

        This method prioritizes `<pre><code>` blocks which are common in technical
        documentation. It also attempts to find language hints.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, where each dictionary
                                 represents a code snippet with 'language' and 'code'.
        """
        print("\n--- Extracting code snippets from HTML... ---")
        snippets = []
        
        # 1. Standard <pre><code> blocks
        for pre in self.soup.find_all('pre'):
            code_tag = pre.find('code')
            if code_tag:
                # Try to determine the language from class names (e.g., "language-python")
                lang_class = code_tag.get('class', [])
                language = self._find_language(lang_class)
                
                snippets.append({
                    'language': language,
                    'code': code_tag.get_text().strip()
                })
                continue # Avoid double-counting

        # 2. Inline `code` tags (if not inside a <pre>)
        for code in self.soup.find_all('code'):
            if not code.find_parent('pre'):
                snippets.append({
                    'language': None, # Inline code usually doesn't have language specified
                    'code': code.get_text().strip()
                })
        
        print(f"Found {len(snippets)} code snippets.")
        return snippets

    def _find_language(self, class_list: List[str]) -> str:
        """Helper to find a language name from a list of CSS classes."""
        for cls in class_list:
            if cls.startswith('language-'):
                return cls.replace('language-', '').lower()
            if cls.startswith('lang-'):
                return cls.replace('lang-', '').lower()
        return 'plaintext' # Default if no language is found

if __name__ == '__main__':
    print("--- Running Code Snippet Extractor Example ---")

    # Example HTML content from a blog post or documentation page.
    mock_html = '''
    <html>
    <body>
        <h1>My Technical Blog Post</h1>
        <p>Here is how you can implement a simple function in Python:</p>
        <pre><code class="language-python">def hello_world():
        print("Hello, world!")</code></pre>
        <p>You can call it using <code>hello_world()</code>.</p>
        
        <p>And here is a JavaScript example:</p>
        <pre><code class="lang-js">// Simple alert
    function greet() {
        alert('Hello from JavaScript!');
    }</code></pre>

        <p>This is an example of a snippet with no language specified:</p>
        <pre><code>
    This is a generic code block.
    It could be a shell command or anything else.
        </code></pre>
    </body>
    </html>
    '''

    extractor = CodeSnippetExtractor(mock_html)
    extracted_snippets = extractor.extract_snippets()

    print("\n--- Extracted Snippets ---")
    for i, snippet in enumerate(extracted_snippets):
        print(f"\n--- Snippet {i+1} (Language: {snippet['language']}) ---")
        print(snippet['code'])
