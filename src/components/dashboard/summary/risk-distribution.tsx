
import { PieChart } from "@/components/ui/chart";

interface RiskDistributionProps {
  data: {
    labels: string[];
    data: number[];
  };
}

export function RiskDistribution({ data }: RiskDistributionProps) {
  return (
    <div>
      <h3 className="text-sm font-semibold mb-3">Risk Distribution</h3>
      <div className="h-[200px] w-full">
        <PieChart
          data={{
            labels: data.labels,
            datasets: [
              {
                data: data.data,
                backgroundColor: ['#3b82f6', '#f59e0b', '#f97316', '#ef4444'],
              },
            ],
          }}
        />
      </div>
    </div>
  );
}
