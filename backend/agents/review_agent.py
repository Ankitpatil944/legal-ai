from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import re
from datetime import datetime

class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{1,2}-\d{1,2}-\d{2,4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
        ]

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract key legal terms, parties, dates, and obligations from the document.
        """
        # Extract parties
        parties = await self._extract_parties(document_text)
        
        # Extract dates
        dates = await self._extract_dates(document_text)
        
        # Extract obligations
        obligations = await self._extract_obligations(document_text)
        
        # Extract key terms
        key_terms = await self._extract_key_terms(document_text)

        return {
            'parties': parties,
            'dates': dates,
            'obligations': obligations,
            'key_terms': key_terms
        }

    async def _extract_parties(self, text: str) -> List[Dict[str, str]]:
        prompt = f"""
        Extract all parties mentioned in the following legal document. For each party, identify:
        1. Party name
        2. Party type (e.g., individual, corporation, government entity)
        3. Role in the document (e.g., plaintiff, defendant, contractor, client)

        Document text:
        {text}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        # Parse the response and structure it
        # This is a simplified version - you might want to add more sophisticated parsing
        parties = []
        for line in response.split('\n'):
            if ':' in line:
                name, details = line.split(':', 1)
                parties.append({
                    'name': name.strip(),
                    'details': details.strip()
                })
        return parties

    async def _extract_dates(self, text: str) -> List[Dict[str, str]]:
        dates = []
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                date_str = match.group()
                try:
                    # Try to parse the date
                    if '/' in date_str:
                        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                    elif '-' in date_str:
                        date_obj = datetime.strptime(date_str, '%m-%d-%Y')
                    else:
                        date_obj = datetime.strptime(date_str, '%B %d %Y')
                    
                    dates.append({
                        'date': date_obj.strftime('%Y-%m-%d'),
                        'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
                    })
                except ValueError:
                    continue
        return dates

    async def _extract_obligations(self, text: str) -> List[Dict[str, str]]:
        prompt = f"""
        Identify all obligations, duties, and responsibilities mentioned in the following legal document.
        For each obligation, identify:
        1. The obligated party
        2. The specific obligation
        3. Any conditions or deadlines associated with the obligation

        Document text:
        {text}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        obligations = []
        for line in response.split('\n'):
            if ':' in line:
                party, obligation = line.split(':', 1)
                obligations.append({
                    'party': party.strip(),
                    'obligation': obligation.strip()
                })
        return obligations

    async def _extract_key_terms(self, text: str) -> List[Dict[str, str]]:
        prompt = f"""
        Identify and explain all important legal terms, definitions, and key concepts in the following document.
        For each term, provide:
        1. The term
        2. Its definition or meaning in the context of the document
        3. Any specific conditions or limitations associated with the term

        Document text:
        {text}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        key_terms = []
        for line in response.split('\n'):
            if ':' in line:
                term, definition = line.split(':', 1)
                key_terms.append({
                    'term': term.strip(),
                    'definition': definition.strip()
                })
        return key_terms 