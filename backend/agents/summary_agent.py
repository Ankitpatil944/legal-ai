from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.summary_sections = [
            'document_type',
            'parties',
            'key_terms',
            'obligations',
            'risks',
            'compliance',
            'recommendations'
        ]

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the document analysis.
        """
        # Generate executive summary
        executive_summary = await self._generate_executive_summary(document_text, context)
        
        # Generate detailed summary
        detailed_summary = await self._generate_detailed_summary(document_text, context)
        
        # Generate key findings
        key_findings = await self._generate_key_findings(context)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(context)

        return {
            'executive_summary': executive_summary,
            'detailed_summary': detailed_summary,
            'key_findings': key_findings,
            'recommendations': recommendations
        }

    async def _generate_executive_summary(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = f"""
        Generate an executive summary of the following legal document analysis:

        Document text:
        {text}

        Analysis context:
        {context if context else 'No additional context provided'}

        Please provide:
        1. Document overview
        2. Key points
        3. Critical issues
        4. Risk assessment
        5. Compliance status
        6. Next steps

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        
        # Parse the response and structure it
        summary = {
            'overview': '',
            'key_points': [],
            'critical_issues': [],
            'risk_assessment': '',
            'compliance_status': '',
            'next_steps': []
        }
        
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'overview' in key:
                    summary['overview'] = value
                elif 'point' in key:
                    summary['key_points'].append(value)
                elif 'issue' in key:
                    summary['critical_issues'].append(value)
                elif 'risk' in key:
                    summary['risk_assessment'] = value
                elif 'compliance' in key:
                    summary['compliance_status'] = value
                elif 'step' in key:
                    summary['next_steps'].append(value)
        
        return summary

    async def _generate_detailed_summary(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt = f"""
        Generate a detailed summary of the following legal document analysis:

        Document text:
        {text}

        Analysis context:
        {context if context else 'No additional context provided'}

        Please provide a comprehensive analysis covering:
        1. Document structure and organization
        2. Detailed analysis of each major section
        3. Legal implications and considerations
        4. Technical details and specifications
        5. Operational requirements
        6. Implementation considerations

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        
        # Parse the response and structure it
        summary = {
            'structure': {},
            'section_analysis': [],
            'legal_implications': [],
            'technical_details': [],
            'operational_requirements': [],
            'implementation_considerations': []
        }
        
        current_section = None
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if 'structure' in key:
                        summary['structure'][key] = value
                    elif 'section' in key:
                        summary['section_analysis'].append(value)
                    elif 'implication' in key:
                        summary['legal_implications'].append(value)
                    elif 'technical' in key:
                        summary['technical_details'].append(value)
                    elif 'operational' in key:
                        summary['operational_requirements'].append(value)
                    elif 'implementation' in key:
                        summary['implementation_considerations'].append(value)
        
        return summary

    async def _generate_key_findings(self, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not context:
            return []

        prompt = f"""
        Generate key findings from the following document analysis:

        Analysis context:
        {context}

        Please provide:
        1. Critical findings
        2. Risk assessment
        3. Compliance issues
        4. Legal implications
        5. Business impact
        6. Recommendations

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        
        # Parse the response and structure it
        findings = []
        current_finding = {}
        
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_finding[key.strip().lower()] = value.strip()
                elif current_finding:
                    findings.append(current_finding)
                    current_finding = {}
        
        if current_finding:
            findings.append(current_finding)
        
        return findings

    async def _generate_recommendations(self, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not context:
            return []

        prompt = f"""
        Generate recommendations based on the following document analysis:

        Analysis context:
        {context}

        Please provide:
        1. Immediate actions required
        2. Short-term improvements
        3. Long-term strategic recommendations
        4. Risk mitigation strategies
        5. Compliance enhancements
        6. Implementation guidance

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        
        # Parse the response and structure it
        recommendations = []
        current_recommendation = {}
        
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_recommendation[key.strip().lower()] = value.strip()
                elif current_recommendation:
                    recommendations.append(current_recommendation)
                    current_recommendation = {}
        
        if current_recommendation:
            recommendations.append(current_recommendation)
        
        return recommendations 