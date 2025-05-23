
import { InfoIcon } from "lucide-react";

interface KeyFindingsProps {
  findings: string[];
}

export function KeyFindings({ findings }: KeyFindingsProps) {
  return (
    <div>
      <h3 className="text-sm font-semibold mb-3">Key Findings</h3>
      <ul className="space-y-2">
        {findings.map((finding, index) => (
          <li key={index} className="flex gap-2 text-sm">
            <InfoIcon className="h-4 w-4 flex-shrink-0 mt-0.5 text-blue-500" />
            <span className="text-muted-foreground">{finding}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
