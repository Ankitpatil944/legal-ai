
import { Badge } from "@/components/ui/badge";

interface DocumentInfoProps {
  documentSummary: {
    title: string;
    type: string;
    parties: string[];
    effectiveDate: string;
    expirationDate: string;
    status: string;
    riskScore: number;
  };
}

export function DocumentInfo({ documentSummary }: DocumentInfoProps) {
  return (
    <div>
      <h3 className="text-sm font-semibold mb-3">Document Information</h3>
      <dl className="space-y-2">
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Title:</dt>
          <dd className="font-medium">{documentSummary.title}</dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Type:</dt>
          <dd className="font-medium">{documentSummary.type}</dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Parties:</dt>
          <dd className="font-medium">{documentSummary.parties.join(", ")}</dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Effective Date:</dt>
          <dd className="font-medium">{documentSummary.effectiveDate}</dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Expiration Date:</dt>
          <dd className="font-medium">{documentSummary.expirationDate}</dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Status:</dt>
          <dd>
            <Badge className="bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
              {documentSummary.status}
            </Badge>
          </dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-muted-foreground">Risk Score:</dt>
          <dd>
            <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300">
              {documentSummary.riskScore}/100
            </Badge>
          </dd>
        </div>
      </dl>
    </div>
  );
}
