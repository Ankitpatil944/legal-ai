from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
import json
from pathlib import Path

class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.compliance_rules_dir = Path("backend/data/compliance_rules")
        self.compliance_rules_dir.mkdir(parents=True, exist_ok=True)
        self.compliance_rules = self._load_compliance_rules()

    def _load_compliance_rules(self) -> Dict[str, Dict[str, Any]]:
        """
        Load compliance rules from JSON files in the compliance_rules directory.
        """
        rules = {}
        for rule_file in self.compliance_rules_dir.glob("*.json"):
            try:
                with open(rule_file, 'r') as f:
                    rule_data = json.load(f)
                    rules[rule_file.stem] = rule_data
            except Exception as e:
                print(f"Error loading compliance rule {rule_file}: {str(e)}")
        return rules

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Check the document for compliance with relevant laws and regulations.
        """
        # Identify applicable jurisdictions and regulations
        jurisdictions = await self._identify_jurisdictions(document_text, context)
        
        # Check compliance with each jurisdiction's rules
        compliance_checks = await self._check_compliance(document_text, jurisdictions)
        
        # Generate compliance report
        compliance_report = await self._generate_compliance_report(compliance_checks)

        return {
            'jurisdictions': jurisdictions,
            'compliance_checks': compliance_checks,
            'compliance_report': compliance_report
        }

    async def _identify_jurisdictions(self, text: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        prompt = f"""
        Identify all relevant jurisdictions and regulations that apply to this legal document.
        Consider:
        1. Geographic locations mentioned
        2. Governing law clauses
        3. Industry-specific regulations
        4. Cross-border implications
        5. Special regulatory requirements

        Document text:
        {text}

        Additional context:
        {context if context else 'No additional context provided'}

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        jurisdictions = []
        
        # Parse the response and structure it
        current_jurisdiction = {}
        for line in response.split('\n'):
            if line.strip():
                if ':' in line:
                    key, value = line.split(':', 1)
                    current_jurisdiction[key.strip().lower()] = value.strip()
                elif current_jurisdiction:
                    jurisdictions.append(current_jurisdiction)
                    current_jurisdiction = {}
        
        if current_jurisdiction:
            jurisdictions.append(current_jurisdiction)
            
        return jurisdictions

    async def _check_compliance(self, text: str, jurisdictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        compliance_checks = []
        
        for jurisdiction in jurisdictions:
            # Get applicable rules for this jurisdiction
            jurisdiction_rules = self.compliance_rules.get(jurisdiction.get('name', '').lower(), {})
            
            prompt = f"""
            Check the following legal document for compliance with {jurisdiction.get('name', '')} regulations.

            Jurisdiction Details:
            {jurisdiction}

            Applicable Rules:
            {jurisdiction_rules}

            Document text:
            {text}

            Please provide:
            1. Compliance status for each rule
            2. Specific violations or concerns
            3. Required changes for compliance
            4. Potential penalties for non-compliance
            5. Recommendations for achieving compliance

            Return the information in a structured format.
            """
            
            response = await self._call_llm(prompt)
            
            # Parse the response and structure it
            compliance_check = {
                'jurisdiction': jurisdiction,
                'status': {},
                'violations': [],
                'required_changes': [],
                'penalties': [],
                'recommendations': []
            }
            
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if 'status' in key:
                        compliance_check['status'][key] = value
                    elif 'violation' in key:
                        compliance_check['violations'].append(value)
                    elif 'change' in key:
                        compliance_check['required_changes'].append(value)
                    elif 'penalty' in key:
                        compliance_check['penalties'].append(value)
                    elif 'recommendation' in key:
                        compliance_check['recommendations'].append(value)
            
            compliance_checks.append(compliance_check)
        
        return compliance_checks

    async def _generate_compliance_report(self, compliance_checks: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = f"""
        Generate a comprehensive compliance report based on the following compliance checks:

        Compliance Checks:
        {compliance_checks}

        Please provide:
        1. Overall compliance status
        2. Summary of key findings
        3. Critical issues requiring immediate attention
        4. Compliance risk assessment
        5. Action items and priorities
        6. Long-term compliance strategy

        Return the information in a structured format.
        """
        
        response = await self._call_llm(prompt)
        
        # Parse the response and structure it
        report = {
            'overall_status': '',
            'key_findings': [],
            'critical_issues': [],
            'risk_assessment': {},
            'action_items': [],
            'long_term_strategy': []
        }
        
        for line in response.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'status' in key:
                    report['overall_status'] = value
                elif 'finding' in key:
                    report['key_findings'].append(value)
                elif 'issue' in key:
                    report['critical_issues'].append(value)
                elif 'risk' in key:
                    report['risk_assessment'][key] = value
                elif 'action' in key:
                    report['action_items'].append(value)
                elif 'strategy' in key:
                    report['long_term_strategy'].append(value)
        
        return report 