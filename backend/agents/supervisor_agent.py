from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent
from .review_agent import ReviewAgent
from .risk_analysis_agent import RiskAnalysisAgent
from .clause_comparison_agent import ClauseComparisonAgent
from .suggestion_agent import SuggestionAgent
from .inconsistency_agent import InconsistencyAgent
from .compliance_agent import ComplianceAgent
from .summary_agent import SummaryAgent

class SupervisorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agents = {
            'review': ReviewAgent(),
            'risk': RiskAnalysisAgent(),
            'clause': ClauseComparisonAgent(),
            'suggestion': SuggestionAgent(),
            'inconsistency': InconsistencyAgent(),
            'compliance': ComplianceAgent(),
            'summary': SummaryAgent()
        }
        self.log_activity("Initialized SupervisorAgent with all sub-agents", "SUCCESS")

    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Orchestrate the document analysis process by coordinating all agents.
        """
        self.log_activity("Starting document analysis process")
        results = {}
        context = context or {}

        try:
            # Step 1: Initial review and extraction
            self.log_activity("Initiating document review phase")
            review_results = await self.agents['review'].process(document_text, context)
            results['review'] = review_results
            context.update(review_results)
            self.log_activity("Document review completed", "SUCCESS")

            # Step 2: Risk analysis
            self.log_activity("Starting risk analysis phase")
            risk_results = await self.agents['risk'].process(document_text, context)
            results['risk'] = risk_results
            context.update(risk_results)
            self.log_activity("Risk analysis completed", "SUCCESS")

            # Step 3: Clause comparison
            self.log_activity("Initiating clause comparison phase")
            clause_results = await self.agents['clause'].process(document_text, context)
            results['clause'] = clause_results
            context.update(clause_results)
            self.log_activity("Clause comparison completed", "SUCCESS")

            # Step 4: Generate suggestions for risky clauses
            if risk_results.get('risky_clauses'):
                self.log_activity("Generating suggestions for risky clauses")
                suggestion_results = await self.agents['suggestion'].process(
                    document_text,
                    {'risky_clauses': risk_results['risky_clauses']}
                )
                results['suggestions'] = suggestion_results
                context.update(suggestion_results)
                self.log_activity("Suggestions generation completed", "SUCCESS")

            # Step 5: Check for inconsistencies
            self.log_activity("Checking for document inconsistencies")
            inconsistency_results = await self.agents['inconsistency'].process(document_text, context)
            results['inconsistencies'] = inconsistency_results
            context.update(inconsistency_results)
            self.log_activity("Inconsistency check completed", "SUCCESS")

            # Step 6: Compliance check
            self.log_activity("Performing compliance check")
            compliance_results = await self.agents['compliance'].process(document_text, context)
            results['compliance'] = compliance_results
            context.update(compliance_results)
            self.log_activity("Compliance check completed", "SUCCESS")

            # Step 7: Generate final summary
            self.log_activity("Generating final document summary")
            summary_results = await self.agents['summary'].process(document_text, context)
            results['summary'] = summary_results
            self.log_activity("Summary generation completed", "SUCCESS")

            self.log_activity("Document analysis process completed successfully", "SUCCESS")
            return results

        except Exception as e:
            self.log_activity(f"Error during document analysis: {str(e)}", "ERROR")
            raise

    async def process_specific_agent(self, agent_name: str, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the document using a specific agent.
        """
        if agent_name not in self.agents:
            self.log_activity(f"Unknown agent requested: {agent_name}", "ERROR")
            raise ValueError(f"Unknown agent: {agent_name}")
        
        self.log_activity(f"Processing document with {agent_name} agent")
        try:
            result = await self.agents[agent_name].process(document_text, context)
            self.log_activity(f"{agent_name} agent processing completed", "SUCCESS")
            return result
        except Exception as e:
            self.log_activity(f"Error in {agent_name} agent: {str(e)}", "ERROR")
            raise 