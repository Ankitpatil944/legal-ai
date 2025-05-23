from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import json
import os
from pathlib import Path

class ClauseComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.templates_dir = Path("backend/data/clause_templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Load clause templates from JSON files in the templates directory.
        """
        templates = {}
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                    templates[template_file.stem] = template_data
            except Exception as e:
                print(f"Error loading template {template_file}: {str(e)}")
        return templates

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Compare document clauses against standard templates.
        """
        # Extract clauses from the document
        clauses = await self._extract_clauses(document_text)
        
        # Compare each clause with templates
        comparisons = await self._compare_clauses(clauses)
        
        # Generate recommendations based on differences
        recommendations = await self._generate_recommendations(comparisons)

        return {
            'clauses': clauses,
            'comparisons': comparisons,
            'recommendations': recommendations
        }

    async def _extract_clauses(self, text: str) -> List[Dict[str, Any]]:
        prompt = f"""
        Extract all distinct clauses from the following legal document.
        For each clause, identify:
        1. The clause text
        2. The clause type (e.g., definition, obligation, limitation, termination)
        3. The section or context where it appears
        4. Any key terms or conditions

        Document text:
        {text}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        clauses = []
        
        # Parse the response and structure it
        current_clause = {}
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_clause[key.strip().lower()] = value.strip()
                elif current_clause:
                    clauses.append(current_clause)
                    current_clause = {}
        
        if current_clause:
            clauses.append(current_clause)
            
        return clauses

    async def _compare_clauses(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        comparisons = []
        
        for clause in clauses:
            clause_type = clause.get('type', '').lower()
            matching_templates = [
                template for name, template in self.templates.items()
                if name.lower() in clause_type or clause_type in name.lower()
            ]
            
            if matching_templates:
                for template in matching_templates:
                    comparison = await self._compare_single_clause(clause, template)
                    comparisons.append(comparison)
            else:
                # If no matching template found, mark for review
                comparisons.append({
                    'clause': clause,
                    'template_match': False,
                    'differences': ['No matching template found'],
                    'recommendation': 'Review clause for standardization'
                })
        
        return comparisons

    async def _compare_single_clause(self, clause: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Compare the following clause with its standard template:

        Clause:
        {clause.get('text', '')}

        Template:
        {template.get('text', '')}

        Please identify:
        1. Key differences between the clause and template
        2. Missing elements from the template
        3. Additional elements not in the template
        4. Potential issues or concerns
        5. Recommendations for alignment

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        
        # Parse the response and structure it
        comparison = {
            'clause': clause,
            'template': template,
            'template_match': True
        }
        
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                comparison[key.strip().lower()] = value.strip()
        
        return comparison

    async def _generate_recommendations(self, comparisons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recommendations = []
        
        for comparison in comparisons:
            if not comparison.get('template_match', False):
                prompt = f"""
                Generate specific recommendations to align the following clause with its standard template:

                Clause:
                {comparison['clause'].get('text', '')}

                Template:
                {comparison['template'].get('text', '')}

                Differences:
                {comparison.get('differences', [])}

                Please provide:
                1. Specific language changes needed
                2. Elements to add or remove
                3. Structural changes required
                4. Any additional considerations

                Return the information in a structured format.
                """
                
                response = await self._call_llm(prompt)
                
                # Parse the response and structure it
                recommendation = {
                    'clause': comparison['clause'],
                    'template': comparison['template']
                }
                
                for line in response.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        recommendation[key.strip().lower()] = value.strip()
                
                recommendations.append(recommendation)
        
        return recommendations 