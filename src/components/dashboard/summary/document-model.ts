
export interface DocumentSummary {
  title: string;
  type: string;
  parties: string[];
  effectiveDate: string;
  expirationDate: string;
  status: string;
  riskScore: number;
  keyFindings: string[];
  sections: {
    name: string;
    riskLevel: string;
  }[];
  riskDistribution: {
    labels: string[];
    data: number[];
  };
  sectionDistribution: {
    labels: string[];
    data: number[];
  };
}
