import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { 
  ChevronLeft, 
  ChevronRight, 
  Maximize, 
  Minimize, 
  ZoomIn, 
  ZoomOut, 
  Share2, 
  Download, 
  Printer
} from "lucide-react";

export function DocumentViewer({ analysis }: { analysis?: any }) {
  const [expanded, setExpanded] = useState(false);
  // Use analysis?.review?.document_text or similar for real data
  const documentText = analysis?.review?.document_text || null;
  return (
    <div className={`glass-panel flex flex-col h-full transition-all duration-300 ${expanded ? 'absolute inset-0 z-50' : 'relative'}`}>
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <ChevronRight className="h-4 w-4" />
          </Button>
          <span className="text-sm font-medium">Page 1 of 10</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <ZoomOut className="h-4 w-4" />
          </Button>
          <span className="text-sm font-medium">100%</span>
          <Button variant="outline" size="icon">
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <Share2 className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <Download className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon">
            <Printer className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon" onClick={() => setExpanded(!expanded)}>
            {expanded ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
          </Button>
        </div>
      </div>

      <div className="flex-1 p-4">
        <Tabs defaultValue="document" className="h-full flex flex-col">
          <TabsList className="grid grid-cols-2 w-[400px] mx-auto mb-4">
            <TabsTrigger value="document">Document</TabsTrigger>
            <TabsTrigger value="comparison">Comparison View</TabsTrigger>
          </TabsList>
          
          <TabsContent value="document" className="flex-1 overflow-auto">
            <div className="bg-white dark:bg-gray-900 rounded-md p-8 shadow-sm border border-border min-h-[500px]">
              {documentText ? (
                <pre className="whitespace-pre-wrap text-sm">{documentText}</pre>
              ) : (
                <>
                  <h2 className="text-xl font-bold mb-4">Employment Agreement</h2>
                  <p className="mb-4 text-sm">This Employment Agreement ("Agreement") is made and entered into as of [Date], by and between [Employer Name], a [State] [entity type] ("Employer") and [Employee Name] ("Employee").</p>
                  <h3 className="font-bold mb-2 text-sm">1. POSITION AND DUTIES</h3>
                  <p className="mb-4 text-sm">
                    1.1. Position. Employee shall serve in the position of [Position Title] or in such other positions as Employer may from time to time assign.
                  </p>
                  <p className="mb-4 text-sm">
                    1.2. Duties. Employee shall perform such duties as are customarily associated with the Employee's position and such other duties as may be assigned from time to time by Employer.
                  </p>
                  <h3 className="font-bold mb-2 text-sm">2. TERM</h3>
                  <p className="mb-4 text-sm">
                    2.1. Initial Term. The initial term of this Agreement shall be for a period of [Term Length] years, commencing on [Start Date] and ending on [End Date] (the "Initial Term").
                  </p>
                  <p className="mb-4 text-sm">
                    2.2. Renewal. Upon expiration of the Initial Term, this Agreement shall automatically renew for successive one-year periods (each a "Renewal Term"), unless either party provides written notice of non-renewal at least [Notice Period] days prior to the end of the Initial Term or any Renewal Term.
                  </p>
                </>
              )}
            </div>
          </TabsContent>
          
          <TabsContent value="comparison" className="flex-1 overflow-auto">
            <div className="grid grid-cols-2 gap-4 h-full">
              <Card>
                <CardContent className="p-4 bg-white dark:bg-gray-900 min-h-[500px]">
                  <h3 className="text-sm font-bold mb-2">Original Version</h3>
                  <div className="text-sm">
                    <p className="mb-3">
                      <span className="bg-yellow-100 dark:bg-yellow-900/30 px-1">1.1. Position. Employee shall serve in the position of [Position Title] or in such other positions as Employer may from time to time assign.</span>
                    </p>
                    <p className="mb-3">
                      2.1. Initial Term. The initial term of this Agreement shall be for a period of [Term Length] years, commencing on [Start Date] and ending on [End Date] (the "Initial Term").
                    </p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 bg-white dark:bg-gray-900 min-h-[500px]">
                  <h3 className="text-sm font-bold mb-2">Revised Version</h3>
                  <div className="text-sm">
                    <p className="mb-3">
                      <span className="bg-green-100 dark:bg-green-900/30 px-1">1.1. Position. Employee shall serve in the position of [Position Title] and shall not be assigned to other positions without Employee's written consent.</span>
                    </p>
                    <p className="mb-3">
                      2.1. Initial Term. The initial term of this Agreement shall be for a period of [Term Length] years, commencing on [Start Date] and ending on [End Date] (the "Initial Term").
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
