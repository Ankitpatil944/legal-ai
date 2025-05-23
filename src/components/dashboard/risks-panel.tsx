import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

type RiskItem = {
  id: string;
  title: string;
  description: string;
  severity: "low" | "medium" | "high" | "critical";
  clause: string;
  page: number;
};

const getSeverityColor = (severity: RiskItem["severity"]) => {
  switch (severity) {
    case "low": return "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
    case "medium": return "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300";
    case "high": return "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300";
    case "critical": return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
    default: return "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300";
  }
};

export function RisksPanel({ analysis }: { analysis?: any }) {
  const risks = analysis?.risk?.risky_clauses || [];
  // If no real risks, fallback to static
  const displayRisks = risks.length > 0 ? risks : [
    {
      id: "risk-1",
      title: "Non-compete duration excessive",
      description: "The non-compete clause duration exceeds typical enforceability standards in most jurisdictions.",
      severity: "high",
      clause: "Section 8.2",
      page: 5,
    },
    {
      id: "risk-2",
      title: "Termination without cause",
      description: "Employer can terminate without cause with minimal notice period.",
      severity: "medium",
      clause: "Section 4.3",
      page: 3,
    },
    {
      id: "risk-3",
      title: "Vague IP assignment",
      description: "Intellectual property assignment language is overly broad and may include pre-existing works.",
      severity: "high",
      clause: "Section 6.1",
      page: 4,
    },
    {
      id: "risk-4",
      title: "Missing arbitration details",
      description: "Arbitration clause does not specify governing rules or arbitration body.",
      severity: "medium",
      clause: "Section 10.4",
      page: 8,
    },
    {
      id: "risk-5",
      title: "Inadequate indemnification",
      description: "Employee indemnification obligations are disproportionate to employer's.",
      severity: "critical",
      clause: "Section 9.2",
      page: 7,
    }
  ];
  return (
    <Card className="glass-panel">
      <CardHeader>
        <CardTitle>Identified Risks</CardTitle>
        <CardDescription>
          Potential legal issues detected in the document
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {displayRisks.map((risk) => (
            <Card key={risk.id} className="hover-scale">
              <CardHeader className="py-3 px-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm font-medium">{risk.title}</CardTitle>
                  <Badge className={`${getSeverityColor(risk.severity)}`}>
                    {risk.severity.charAt(0).toUpperCase() + risk.severity.slice(1)}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="py-2 px-4 text-sm">
                <p className="text-muted-foreground mb-2">{risk.description}</p>
                <div className="flex justify-between items-center mt-4">
                  <div className="flex items-center gap-4">
                    <span className="text-xs py-1 px-2 rounded-full bg-secondary text-secondary-foreground">
                      {risk.clause}
                    </span>
                    <span className="text-xs py-1 px-2 rounded-full bg-secondary text-secondary-foreground">
                      Page {risk.page}
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">Ignore</Button>
                    <Button size="sm" variant="default">View</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
