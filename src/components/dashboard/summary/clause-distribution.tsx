
import { BarChart } from "@/components/ui/chart";

interface ClauseDistributionProps {
  data: {
    labels: string[];
    data: number[];
  };
}

export function ClauseDistribution({ data }: ClauseDistributionProps) {
  return (
    <div>
      <h3 className="text-sm font-semibold mb-3">Clause Distribution</h3>
      <div className="h-[250px] w-full">
        <BarChart
          data={{
            labels: data.labels,
            datasets: [
              {
                label: 'Number of clauses',
                data: data.data,
                backgroundColor: 'rgba(62, 123, 250, 0.6)',
              },
            ],
          }}
        />
      </div>
    </div>
  );
}
