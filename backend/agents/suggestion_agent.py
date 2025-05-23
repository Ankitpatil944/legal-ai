from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent

class SuggestionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.rewriting_guidelines = {
            'clarity': 'Use clear, unambiguous language',
            'specificity': 'Replace vague terms with specific ones',
            'balance': 'Ensure balanced obligations and rights',
            'compliance': 'Ensure regulatory compliance',
            'enforceability': 'Use legally enforceable language'
        }

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate safer alternatives for clauses that need improvement.
        """
        if not context or 'risky_clauses' not in context:
            return {'error': 'No risky clauses provided in context'}

        risky_clauses = context['risky_clauses']
        
        # Generate alternative versions for each risky clause
        alternatives = await self._generate_alternatives(risky_clauses)
        
        # Explain the improvements in each alternative
        explanations = await self._explain_improvements(alternatives)
        
        # Provide implementation guidance
        guidance = await self._generate_implementation_guidance(alternatives)

        return {
            'alternatives': alternatives,
            'explanations': explanations,
            'guidance': guidance
        }

    async def _generate_alternatives(self, risky_clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alternatives = []
        
        for clause in risky_clauses:
            prompt = f"""
            Rewrite the following risky clause to make it safer and more effective:

            Original Clause:
            {clause.get('clause_text', '')}

            Risk/Issue:
            {clause.get('risk', '')}

            Please provide:
            1. A safer alternative version
            2. Key changes made
            3. How the changes address the risk
            4. Any additional considerations

            Follow these guidelines:
            - Use clear, unambiguous language
            - Replace vague terms with specific ones
            - Ensure balanced obligations and rights
            - Maintain regulatory compliance
            - Use legally enforceable language

            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and structure it
            alternative = {
                'original_clause': clause,
                'alternative_version': '',
                'changes': [],
                'risk_addressed': '',
                'considerations': []
            }
            
            current_section = None
            for line in response.split('\n'):
                if line.strip():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if 'alternative' in key:
                            alternative['alternative_version'] = value
                        elif 'change' in key:
                            alternative['changes'].append(value)
                        elif 'risk' in key:
                            alternative['risk_addressed'] = value
                        elif 'consideration' in key:
                            alternative['considerations'].append(value)
            
            alternatives.append(alternative)
        
        return alternatives

    async def _explain_improvements(self, alternatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        explanations = []
        
        for alternative in alternatives:
            prompt = f"""
            Explain the improvements in the following clause revision:

            Original Clause:
            {alternative['original_clause'].get('clause_text', '')}

            Alternative Version:
            {alternative['alternative_version']}

            Changes Made:
            {alternative['changes']}

            Please provide:
            1. Detailed explanation of each improvement
            2. Legal benefits of the changes
            3. How the changes enhance clarity and enforceability
            4. Any potential trade-offs or considerations

            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and structure it
            explanation = {
                'alternative': alternative,
                'improvements': [],
                'legal_benefits': [],
                'enhancements': [],
                'considerations': []
            }
            
            current_section = None
            for line in response.split('\n'):
                if line.strip():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if 'improvement' in key:
                            explanation['improvements'].append(value)
                        elif 'benefit' in key:
                            explanation['legal_benefits'].append(value)
                        elif 'enhancement' in key:
                            explanation['enhancements'].append(value)
                        elif 'consideration' in key:
                            explanation['considerations'].append(value)
            
            explanations.append(explanation)
        
        return explanations

    async def _generate_implementation_guidance(self, alternatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        guidance = []
        
        for alternative in alternatives:
            prompt = f"""
            Provide implementation guidance for the following clause revision:

            Original Clause:
            {alternative['original_clause'].get('clause_text', '')}

            Alternative Version:
            {alternative['alternative_version']}

            Please provide:
            1. Step-by-step implementation instructions
            2. Required changes to related clauses
            3. Potential impact on other parts of the document
            4. Recommended review and approval process
            5. Any additional documentation needed

            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and structure it
            implementation = {
                'alternative': alternative,
                'steps': [],
                'related_changes': [],
                'impacts': [],
                'review_process': [],
                'documentation': []
            }
            
            current_section = None
            for line in response.split('\n'):
                if line.strip():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if 'step' in key:
                            implementation['steps'].append(value)
                        elif 'related' in key:
                            implementation['related_changes'].append(value)
                        elif 'impact' in key:
                            implementation['impacts'].append(value)
                        elif 'review' in key:
                            implementation['review_process'].append(value)
                        elif 'documentation' in key:
                            implementation['documentation'].append(value)
            
            guidance.append(implementation)
        
        return guidance 