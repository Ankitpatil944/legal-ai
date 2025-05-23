
export function AIInsights() {
  return (
    <>
      <p>
        This employment agreement contains several clauses that may present legal challenges in certain jurisdictions.
        The most significant concerns are:
      </p>
      
      <div className="space-y-2">
        <h4 className="font-semibold text-sm">1. Non-compete Restrictions</h4>
        <p className="text-muted-foreground">
          The non-compete duration of 2 years exceeds typically enforceable limits in many states. 
          Consider reducing to 1 year and adding geographic limitations.
        </p>
      </div>
      
      <div className="space-y-2">
        <h4 className="font-semibold text-sm">2. Intellectual Property Provisions</h4>
        <p className="text-muted-foreground">
          The IP assignment language is overly broad and may inadvertently capture personal projects 
          or inventions created outside of employment.
        </p>
      </div>
      
      <div className="space-y-2">
        <h4 className="font-semibold text-sm">3. Termination Clauses</h4>
        <p className="text-muted-foreground">
          The 7-day notice period for termination without cause is shorter than industry standards 
          and may create employee retention risks.
        </p>
      </div>
      
      <div className="space-y-2">
        <h4 className="font-semibold text-sm">4. Indemnification Imbalance</h4>
        <p className="text-muted-foreground">
          The indemnification obligations heavily favor the employer, creating potential 
          liability concerns for the employee.
        </p>
      </div>
      
      <div className="mt-6 p-3 bg-blue-50 dark:bg-blue-950/20 rounded-md">
        <p className="font-medium text-blue-700 dark:text-blue-400 mb-1">Recommended Actions:</p>
        <ul className="list-disc pl-5 space-y-1 text-sm text-blue-700 dark:text-blue-400">
          <li>Review non-compete with jurisdiction-specific counsel</li>
          <li>Narrow IP assignment language to work-related inventions</li>
          <li>Extend termination notice period to at least 30 days</li>
          <li>Balance indemnification obligations</li>
        </ul>
      </div>
    </>
  );
}
