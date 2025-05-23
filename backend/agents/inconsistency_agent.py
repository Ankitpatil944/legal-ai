from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent

class InconsistencyAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.inconsistency_types = {
            'temporal': 'Conflicting dates or timeframes',
            'obligation': 'Conflicting obligations or requirements',
            'definition': 'Inconsistent definitions or terms',
            'scope': 'Conflicting scope or coverage',
            'condition': 'Conflicting conditions or prerequisites'
        }

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Identify and analyze inconsistencies in the document.
        """
        # Identify potential inconsistencies
        inconsistencies = await self._identify_inconsistencies(document_text)
        
        # Analyze the impact of each inconsistency
        impact_analysis = await self._analyze_impact(inconsistencies)
        
        # Generate resolution recommendations
        recommendations = await self._generate_resolutions(inconsistencies)

        return {
            'inconsistencies': inconsistencies,
            'impact_analysis': impact_analysis,
            'recommendations': recommendations
        }

    async def _identify_inconsistencies(self, text: str) -> List[Dict[str, Any]]:
        prompt = f"""
        Analyze the following legal document for inconsistencies and conflicts.
        Look for:
        1. Conflicting dates or timeframes
        2. Contradictory obligations or requirements
        3. Inconsistent definitions or terms
        4. Conflicting scope or coverage
        5. Contradictory conditions or prerequisites

        For each inconsistency found, provide:
        - The conflicting elements
        - Where they appear in the document
        - The type of inconsistency
        - The potential impact

        Document text:
        {text}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        inconsistencies = []
        
        # Parse the response and structure it
        current_inconsistency = {}
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_inconsistency[key.strip().lower()] = value.strip()
                elif current_inconsistency:
                    inconsistencies.append(current_inconsistency)
                    current_inconsistency = {}
        
        if current_inconsistency:
            inconsistencies.append(current_inconsistency)
            
        return inconsistencies

    async def _analyze_impact(self, inconsistencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        impact_analysis = []
        
        for inconsistency in inconsistencies:
            prompt = f"""
            Analyze the impact of the following inconsistency in the legal document:

            Inconsistency Type: {inconsistency.get('type', '')}
            Conflicting Elements: {inconsistency.get('elements', '')}
            Location: {inconsistency.get('location', '')}

            Please provide:
            1. Severity of the impact (High/Medium/Low)
            2. Potential legal consequences
            3. Effect on document enforceability
            4. Impact on parties' rights and obligations
            5. Risk of disputes or litigation

            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and structure it
            analysis = {
                'inconsistency': inconsistency,
                'severity': '',
                'consequences': [],
                'enforceability_impact': '',
                'rights_impact': [],
                'litigation_risk': ''
            }
            
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if 'severity' in key:
                        analysis['severity'] = value
                    elif 'consequence' in key:
                        analysis['consequences'].append(value)
                    elif 'enforceability' in key:
                        analysis['enforceability_impact'] = value
                    elif 'right' in key:
                        analysis['rights_impact'].append(value)
                    elif 'litigation' in key:
                        analysis['litigation_risk'] = value
            
            impact_analysis.append(analysis)
        
        return impact_analysis

    async def _generate_resolutions(self, inconsistencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recommendations = []
        
        for inconsistency in inconsistencies:
            prompt = f"""
            Generate resolution recommendations for the following inconsistency:

            Inconsistency Type: {inconsistency.get('type', '')}
            Conflicting Elements: {inconsistency.get('elements', '')}
            Location: {inconsistency.get('location', '')}

            Please provide:
            1. Specific language changes needed
            2. Alternative approaches to resolve the conflict
            3. Required modifications to related provisions
            4. Implementation steps
            5. Additional considerations or precautions

            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and structure it
            recommendation = {
                'inconsistency': inconsistency,
                'language_changes': [],
                'alternatives': [],
                'modifications': [],
                'steps': [],
                'considerations': []
            }
            
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if 'language' in key:
                        recommendation['language_changes'].append(value)
                    elif 'alternative' in key:
                        recommendation['alternatives'].append(value)
                    elif 'modification' in key:
                        recommendation['modifications'].append(value)
                    elif 'step' in key:
                        recommendation['steps'].append(value)
                    elif 'consideration' in key:
                        recommendation['considerations'].append(value)
            
            recommendations.append(recommendation)
        
        return recommendations 