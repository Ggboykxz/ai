# --- NEXUS_AI_SYSTEM/06_SAFETY_ALIGNMENT_SYSTEM/content_moderation/sensitive_data_scanner.py ---

import re
from typing import List, Dict, Pattern

class SensitiveDataScanner:
    """
    Scans text content to detect potential leaks of sensitive information
    like API keys, passwords, and private identifiers.

    This is a critical component of the Safety & Alignment System to prevent the model
    from inadvertently exposing secrets in its generated or modified code.
    """

    def __init__(self):
        """
        Initializes the scanner with a set of predefined regex patterns for common secrets.
        """
        # This is a basic set of patterns. A real-world system would have a more
        # comprehensive and configurable set.
        self.patterns: Dict[str, Pattern] = {
            'AWS_API_KEY': re.compile(r'AKIA[0-9A-Z]{16}'),
            'GOOGLE_API_KEY': re.compile(r'AIza[0-9A-Za-z\-_]{35}'),
            'GITHUB_TOKEN': re.compile(r'ghp_[0-9a-zA-Z]{36}'),
            'SLACK_TOKEN': re.compile(r'xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}'),
            'PRIVATE_KEY': re.compile(r'-----BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY-----'),
            'GENERIC_SECRET': re.compile(r'['"`][sS][eE][cC][rR][eE][tT]['"`]\s*[:=]\s*['"`][^\s'"`]+['"`]')
        }

    def scan_content(self, content: str) -> List[Dict]:
        """
        Scans the provided string content against all registered patterns.

        Args:
            content (str): The text or code to be scanned.

        Returns:
            List[Dict]: A list of findings. Each finding is a dictionary containing
                        the type of secret, the matched value, and its location (line number).
        """
        print("\n--- Scanning content for sensitive data... ---")
        findings = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for secret_type, pattern in self.patterns.items():
                match = pattern.search(line)
                if match:
                    finding = {
                        'line': line_num,
                        'type': secret_type,
                        'match': self._mask_match(match.group(0), secret_type),
                        'description': f"Found a potential '{secret_type}' on line {line_num}."
                    }
                    findings.append(finding)
        
        if findings:
            print(f"Found {len(findings)} potential secrets.")
        else:
            print("No sensitive data found.")
            
        return findings

    def _mask_match(self, match_value: str, secret_type: str) -> str:
        """
        Masks the found secret, showing only a preview.
        """
        if secret_type == 'PRIVATE_KEY':
            return f"{match_value[:30]}..."
        
        if len(match_value) < 8:
            return "***"
        
        return f"{match_value[:4]}...{match_value[-4:]}"

if __name__ == '__main__':
    print("--- Running Sensitive Data Scanner Example ---")

    # Example code containing various secrets
    code_with_secrets = '''
    # Configuration file

    API_KEY = "AIzaSyA...-T8o" # This is a Google API Key
    aws_access_key = "AKIAIOSFODNN7EXAMPLE"

    def connect_to_slack():
        # Do not commit this!
        token = "xoxb-123456789012-123456789012-123456789012-abcdef1234567890abcdef12345678"
        print(f"Using token: {token}")

    my_secret = 'my_super_secret_password' # Generic secret pattern

    github_pat = "ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"

    cert = """-----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEA ... many lines of key data ...
    -----END RSA PRIVATE KEY-----"""

    '''

    scanner = SensitiveDataScanner()
    scan_results = scanner.scan_content(code_with_secrets)

    print("\n--- Scan Results ---")
    if scan_results:
        for f in scan_results:
            print(f"- {f['description']} (Match: {f['match']})")
    else:
        print("No issues detected.")
