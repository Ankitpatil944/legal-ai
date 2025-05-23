from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent

class RiskAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.risk_indicators = [
            "reasonable",
            "best efforts",
            "material",
            "substantial",
            "significant",
            "as soon as possible",
            "in a timely manner",
            "shall",
            "may",
            "at the discretion of",
            "subject to",
            "without limitation",
            "including but not limited to"
        ]

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze the document for risky or ambiguous clauses.
        """
        # Identify potentially risky clauses
        risky_clauses = await self._identify_risky_clauses(document_text)
        
        # Analyze the severity of each risk
        risk_analysis = await self._analyze_risk_severity(risky_clauses)
        
        # Generate recommendations for risk mitigation
        recommendations = await self._generate_risk_recommendations(risky_clauses)

        return {
            'risky_clauses': risky_clauses,
            'risk_analysis': risk_analysis,
            'recommendations': recommendations
        }

    async def _identify_risky_clauses(self, text: str) -> List[Dict[str, Any]]:
        prompt = f"""
        Analyze the following legal document and identify clauses that contain:
        1. Vague or ambiguous language
        2. Unclear obligations or responsibilities
        3. Potentially problematic terms or conditions
        4. Missing or incomplete information
        5. Unbalanced or unfair provisions

        For each identified clause, provide:
        - The clause text
        - The specific risk or concern
        - The potential impact
        - The section or context where it appears

        Document text:
        {text}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        risky_clauses = []
        
        # Parse the response and structure it
        current_clause = {}
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_clause[key.strip().lower()] = value.strip()
                elif current_clause:
                    risky_clauses.append(current_clause)
                    current_clause = {}
        
        if current_clause:
            risky_clauses.append(current_clause)
            
        return risky_clauses

    async def _analyze_risk_severity(self, risky_clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        risk_analysis = []
        
        for clause in risky_clauses:
            prompt = f"""
            Analyze the severity of the following risky clause in a legal document:
            
            Clause: {clause.get('clause_text', '')}
            Risk: {clause.get('risk', '')}
            Impact: {clause.get('impact', '')}
            
            Please provide:
            1. Risk severity level (High/Medium/Low)
            2. Justification for the severity rating
            3. Potential legal implications
            4. Suggested mitigation strategies
            
            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and add to analysis
            analysis = {'clause': clause}
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    analysis[key.strip().lower()] = value.strip()
            
            risk_analysis.append(analysis)
            
        return risk_analysis

    async def _generate_risk_recommendations(self, risky_clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recommendations = []
        
        for clause in risky_clauses:
            prompt = f"""
            Generate specific recommendations to address the following risky clause:
            
            Clause: {clause.get('clause_text', '')}
            Risk: {clause.get('risk', '')}
            Impact: {clause.get('impact', '')}
            
            Please provide:
            1. Specific language changes or additions
            2. Alternative clause formulations
            3. Additional provisions that should be included
            4. Any necessary definitions or clarifications
            
            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and add to recommendations
            recommendation = {'clause': clause}
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    recommendation[key.strip().lower()] = value.strip()
            
            recommendations.append(recommendation)
            
        return recommendations 