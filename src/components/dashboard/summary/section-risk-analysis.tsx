
import { Badge } from "@/components/ui/badge";

interface Section {
  name: string;
  riskLevel: string;
}

interface SectionRiskAnalysisProps {
  sections: Section[];
}

export function SectionRiskAnalysis({ sections }: SectionRiskAnalysisProps) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case "low": return "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
      case "medium": return "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300";
      case "high": return "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300";
      case "critical": return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
      default: return "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300";
    }
  };

  return (
    <div>
      <h3 className="text-sm font-semibold mb-3">Section Risk Analysis</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-2">
        {sections.map((section, index) => (
          <div key={index} className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">{section.name}</span>
            <Badge className={`${getRiskColor(section.riskLevel)}`}>
              {section.riskLevel.charAt(0).toUpperCase() + section.riskLevel.slice(1)}
            </Badge>
          </div>
        ))}
      </div>
    </div>
  );
}
