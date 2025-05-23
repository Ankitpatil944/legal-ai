import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { DocumentInfo } from "./summary/document-info";
import { KeyFindings } from "./summary/key-findings";
import { SectionRiskAnalysis } from "./summary/section-risk-analysis";
import { RiskDistribution } from "./summary/risk-distribution";
import { ClauseDistribution } from "./summary/clause-distribution";
import { AIInsights } from "./summary/ai-insights";
import { DocumentSummary } from "./summary/document-model";

export function SummaryPanel({ analysis }: { analysis?: any }) {
  const documentSummary = analysis?.summary || {
    title: "Employment Agreement",
    type: "Contract",
    parties: ["Employer Corp.", "Jane Doe"],
    effectiveDate: "2023-05-15",
    expirationDate: "2025-05-14",
    status: "Active",
    riskScore: 65,
    keyFindings: [
      "Non-compete clause may have enforceability issues",
      "Termination provisions favor employer",
      "Intellectual property assignment is overly broad",
      "Missing arbitration details",
      "Indemnification obligations are unbalanced",
    ],
    sections: [
      { name: "Employment Terms", riskLevel: "low" },
      { name: "Compensation", riskLevel: "low" },
      { name: "Termination", riskLevel: "medium" },
      { name: "Confidentiality", riskLevel: "low" },
      { name: "Non-competition", riskLevel: "high" },
      { name: "Intellectual Property", riskLevel: "high" },
      { name: "Indemnification", riskLevel: "critical" },
      { name: "General Provisions", riskLevel: "low" },
    ],
    riskDistribution: {
      labels: ["Low", "Medium", "High", "Critical"],
      data: [3, 2, 2, 1],
    },
    sectionDistribution: {
      labels: ["Terms", "Comp", "Term", "Conf", "Non-comp", "IP", "Indem", "Gen"],
      data: [12, 8, 10, 15, 7, 9, 5, 14],
    },
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <Card className="glass-panel lg:col-span-2">
        <CardHeader>
          <CardTitle>Document Summary</CardTitle>
          <CardDescription>Key information and analysis results</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <DocumentInfo documentSummary={documentSummary} />
            <KeyFindings findings={documentSummary.keyFindings} />
            <SectionRiskAnalysis sections={documentSummary.sections} />
            <RiskDistribution data={documentSummary.riskDistribution} />
          </div>
          
          <div className="mt-6">
            <ClauseDistribution data={documentSummary.sectionDistribution} />
          </div>
        </CardContent>
      </Card>
      
      <Card className="glass-panel">
        <CardHeader>
          <CardTitle>AI Insights</CardTitle>
          <CardDescription>Generated observations and insights</CardDescription>
        </CardHeader>
        <CardContent className="text-sm space-y-4">
          <AIInsights />
        </CardContent>
      </Card>
    </div>
  );
}
