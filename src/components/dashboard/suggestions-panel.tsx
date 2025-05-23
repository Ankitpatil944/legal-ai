import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Check, ArrowRight, X } from "lucide-react";

type SuggestionItem = {
  id: string;
  title: string;
  description: string;
  originalText: string;
  suggestedText: string;
  clause: string;
  page: number;
};

export function SuggestionsPanel({ analysis }: { analysis?: any }) {
  const [acceptedSuggestions, setAcceptedSuggestions] = useState<string[]>([]);
  const [rejectedSuggestions, setRejectedSuggestions] = useState<string[]>([]);

  const handleAccept = (id: string) => {
    setAcceptedSuggestions([...acceptedSuggestions, id]);
    setRejectedSuggestions(rejectedSuggestions.filter(item => item !== id));
  };

  const handleReject = (id: string) => {
    setRejectedSuggestions([...rejectedSuggestions, id]);
    setAcceptedSuggestions(acceptedSuggestions.filter(item => item !== id));
  };

  const getSuggestionStatus = (id: string) => {
    if (acceptedSuggestions.includes(id)) return "accepted";
    if (rejectedSuggestions.includes(id)) return "rejected";
    return "pending";
  };

  const suggestions = analysis?.suggestions?.suggestions || [
    {
      id: "suggestion-1",
      title: "Improve non-compete clause clarity",
      description: "Add specific geographical limitations to the non-compete clause.",
      originalText: "Employee shall not engage in any competing business within the market for a period of two years.",
      suggestedText: "Employee shall not engage in any competing business within a 50-mile radius of Employer's principal place of business for a period of one year.",
      clause: "Section 8.2",
      page: 5,
    },
    {
      id: "suggestion-2",
      title: "Enhance termination notice period",
      description: "Increase notice period for termination without cause.",
      originalText: "Employer may terminate this Agreement without cause with 7 days' notice.",
      suggestedText: "Employer may terminate this Agreement without cause with 30 days' written notice.",
      clause: "Section 4.3",
      page: 3,
    },
    {
      id: "suggestion-3",
      title: "Clarify intellectual property scope",
      description: "Limit IP assignment to work-related inventions only.",
      originalText: "Employee assigns all inventions to Employer.",
      suggestedText: "Employee assigns all inventions created during employment and related to Employer's business to Employer.",
      clause: "Section 6.1",
      page: 4,
    }
  ];

  return (
    <Card className="glass-panel">
      <CardHeader>
        <CardTitle>AI Suggestions</CardTitle>
        <CardDescription>
          Recommended improvements to enhance contract clarity and reduce risk
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {suggestions.map((suggestion) => {
            const status = getSuggestionStatus(suggestion.id);
            return (
              <Card 
                key={suggestion.id} 
                className={`hover-scale ${
                  status === "accepted" ? "border-green-500" : 
                  status === "rejected" ? "border-red-500" : ""
                }`}
              >
                <CardHeader className="py-3 px-4">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-medium">{suggestion.title}</CardTitle>
                    {status === "accepted" && (
                      <Badge className="bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
                        Accepted
                      </Badge>
                    )}
                    {status === "rejected" && (
                      <Badge className="bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
                        Rejected
                      </Badge>
                    )}
                  </div>
                  <CardDescription className="text-xs mt-1">
                    {suggestion.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="py-2 px-4 text-sm">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 dark:bg-gray-900/50 p-3 rounded-md">
                      <p className="text-xs font-medium mb-1">Original Text:</p>
                      <p className="text-xs text-muted-foreground">{suggestion.originalText}</p>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-900/50 p-3 rounded-md">
                      <p className="text-xs font-medium mb-1">Suggested Text:</p>
                      <p className="text-xs text-muted-foreground">{suggestion.suggestedText}</p>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center mt-4">
                    <div className="flex items-center gap-4">
                      <span className="text-xs py-1 px-2 rounded-full bg-secondary text-secondary-foreground">
                        {suggestion.clause}
                      </span>
                      <span className="text-xs py-1 px-2 rounded-full bg-secondary text-secondary-foreground">
                        Page {suggestion.page}
                      </span>
                    </div>
                    {status === "pending" && (
                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-red-600 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-950/20"
                          onClick={() => handleReject(suggestion.id)}
                        >
                          <X className="h-4 w-4 mr-1" /> Reject
                        </Button>
                        <Button 
                          size="sm"
                          className="bg-green-600 text-white hover:bg-green-700"
                          onClick={() => handleAccept(suggestion.id)}
                        >
                          <Check className="h-4 w-4 mr-1" /> Accept
                        </Button>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

// Missing import for Badge component
import { Badge } from "@/components/ui/badge";
