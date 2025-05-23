import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  FileText, 
  Info 
} from "lucide-react";

export function AnalyticsPanel({ analysis }: { analysis?: any }) {
  // Example: use analysis?.summary or analysis?.review for real data
  const docType = analysis?.review?.document_type || "Employment Contract";
  const pages = analysis?.review?.pages || 10;
  const clauses = analysis?.review?.clauses?.length || 24;
  const riskScore = analysis?.risk?.score || "Medium (65/100)";
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <Card className="glass-panel hover-scale">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Analysis Progress</CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-muted-foreground">Processing document...</span>
            <span className="text-xs font-medium">75%</span>
          </div>
          <Progress value={75} className="h-2" />
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="flex flex-col items-center">
              <div className="flex items-center gap-1">
                <CheckCircle2 className="h-3 w-3 text-green-500" />
                <span className="text-xs">Completed</span>
              </div>
              <span className="text-lg font-semibold">12</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="flex items-center gap-1">
                <Clock className="h-3 w-3 text-amber-500" />
                <span className="text-xs">In Progress</span>
              </div>
              <span className="text-lg font-semibold">3</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="flex items-center gap-1">
                <AlertTriangle className="h-3 w-3 text-red-500" />
                <span className="text-xs">Issues</span>
              </div>
              <span className="text-lg font-semibold">2</span>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card className="glass-panel hover-scale">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Document Overview</CardTitle>
          <FileText className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Info className="h-4 w-4 text-blue-500" />
                <span className="text-xs">Document Type:</span>
              </div>
              <span className="text-xs font-medium">{docType}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Info className="h-4 w-4 text-blue-500" />
                <span className="text-xs">Pages:</span>
              </div>
              <span className="text-xs font-medium">{pages}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Info className="h-4 w-4 text-blue-500" />
                <span className="text-xs">Clauses:</span>
              </div>
              <span className="text-xs font-medium">{clauses}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-red-500" />
                <span className="text-xs">Risk Score:</span>
              </div>
              <span className="text-xs font-medium">{riskScore}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
