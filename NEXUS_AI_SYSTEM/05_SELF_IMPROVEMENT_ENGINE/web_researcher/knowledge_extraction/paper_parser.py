# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/web_research/knowledge_extraction/paper_parser.py ---

import re
from typing import Dict, List

class PaperParser:
    """
    A simple parser for extracting structured information from the raw text of a scientific paper.
    
    This parser uses regular expressions to identify common sections of a research paper,
    such as Title, Abstract, Introduction, Conclusion, and References.
    It serves as a foundational tool for the knowledge synthesis step.
    """

    def __init__(self, raw_text: str):
        """
        Initializes the parser with the raw text content of a paper.

        Args:
            raw_text (str): The full text content of the paper.
        """
        self.text = raw_text
        self.sections: Dict[str, str] = {}

    def parse(self) -> Dict[str, str]:
        """
        Parses the raw text to identify and extract distinct sections.

        Returns:
            Dict[str, str]: A dictionary where keys are section titles (lowercased) 
                            and values are the content of those sections.
        """
        print("\n--- Parsing raw paper text... ---")
        # A pattern to find common section headers (e.g., "1. Introduction", "Abstract")
        # This pattern looks for lines that are likely to be headers.
        # It captures the section title and the content that follows.
        pattern = re.compile(
            r"(^(?:[0-9]+\.\s+|)\b(Abstract|Introduction|Conclusion|Related Work|Method|Methodology|Experiment|Results|Discussion|References)\b.*?$)"
            r"([\s\S]*?)"
            r"(?=^(?:[0-9]+\.\s+|)\b(Abstract|Introduction|Conclusion|Related Work|Method|Methodology|Experiment|Results|Discussion|References|Acknowle|Appendix)\b.*?$)",
            re.MULTILINE | re.IGNORECASE
        )

        matches = pattern.findall(self.text + "\nConclusion") # Add a sentinel

        if not matches:
            # If the main pattern fails, try a simpler approach for the abstract
            self._parse_abstract_fallback()
            print("Could not parse full sections, attempting fallback for abstract.")
            return self.sections

        for header, title, content in matches:
            # Normalize the title: take the core word, lowercase it.
            clean_title = title.lower().strip()
            self.sections[clean_title] = content.strip()
        
        print(f"Successfully parsed {len(self.sections)} sections.")
        return self.sections

    def _parse_abstract_fallback(self):
        """
        A fallback method to extract just the abstract if structured parsing fails.
        """
        abstract_match = re.search(r"\bAbstract\b([\s\S]*?)(?:\n\n|\b1\.\s*Introduction\b)", self.text, re.IGNORECASE | re.DOTALL)
        if abstract_match:
            self.sections['abstract'] = abstract_match.group(1).strip()

    def get_section(self, section_name: str) -> str:
        """
        Retrieves the content of a specific section.

        Args:
            section_name (str): The name of the section (e.g., 'introduction').

        Returns:
            str: The content of the section, or an empty string if not found.
        """
        return self.sections.get(section_name.lower(), "")

if __name__ == '__main__':
    print("--- Running Paper Parser Example ---")

    # A mock paper text simulating the structure of a real paper.
    mock_paper_text = """
    A Simple and Effective Paper Title

    John Doe, Jane Smith

    Abstract
    This is the abstract of the paper. It summarizes the key findings.
    It usually comes before the main body of the text.

    1. Introduction
    This is the introduction section. It provides background information and states the research question.
    It contains several paragraphs.

    2. Methodology
    Here we describe the methods used in our study. This includes the dataset,
    the model architecture, and the training procedure.

    3. Results
    This section presents the results of the experiments. We often include tables and figures here.
    Our model achieved state-of-the-art performance.

    4. Conclusion
    This is the conclusion. We summarize our contributions and suggest future work.

    References
    [1] A. Vaswani et al. Attention Is All You Need. 2017.
    [2] J. Devlin et al. BERT: Pre-training of Deep Bidirectional Transformers. 2018.
    """

    parser = PaperParser(mock_paper_text)
    parsed_sections = parser.parse()

    print("\n--- Parsed Sections ---")
    for title, _ in parsed_sections.items():
        print(f"- Found section: {title}")

    print("\n--- Content of 'Introduction' Section ---")
    introduction = parser.get_section('introduction')
    print(introduction)
    
    print("\n--- Content of 'Abstract' Section ---")
    abstract = parser.get_section('abstract')
    print(abstract)
