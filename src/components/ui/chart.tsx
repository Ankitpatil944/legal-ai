
import React from "react";
import { LineChart as RechartsLineChart, BarChart as RechartsBarChart, PieChart as RechartsPieChart, Line, Bar, Pie, Cell, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

// Base chart configuration for consistency
const chartConfig = {
  margin: { top: 5, right: 30, left: 20, bottom: 5 }
};

// Line chart component
export const LineChart = ({ data }: { data: any }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsLineChart
        data={data.datasets[0].data.map((value: any, index: number) => ({
          name: data.labels[index],
          value
        }))}
        margin={chartConfig.margin}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#8884d8"
          activeDot={{ r: 8 }}
        />
      </RechartsLineChart>
    </ResponsiveContainer>
  );
};

// Bar chart component
export const BarChart = ({ data }: { data: any }) => {
  // Transform the data format to match recharts requirements
  const transformedData = data.labels.map((label: string, index: number) => {
    const dataPoint: any = { name: label };
    data.datasets.forEach((dataset: any, datasetIndex: number) => {
      dataPoint[dataset.label || `Dataset ${datasetIndex}`] = dataset.data[index];
    });
    return dataPoint;
  });

  return (
    <ResponsiveContainer width="100%" height={250}>
      <RechartsBarChart
        data={transformedData}
        margin={chartConfig.margin}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        {data.datasets.map((dataset: any, index: number) => (
          <Bar
            key={index}
            dataKey={dataset.label || `Dataset ${index}`}
            fill={dataset.backgroundColor || `#${Math.floor(Math.random()*16777215).toString(16)}`}
            animationDuration={1000}
            animationEasing="ease-out"
          />
        ))}
      </RechartsBarChart>
    </ResponsiveContainer>
  );
};

// Pie chart component
export const PieChart = ({ data }: { data: any }) => {
  // Transform the data format to match recharts requirements
  const transformedData = data.labels.map((label: string, index: number) => ({
    name: label,
    value: data.datasets[0].data[index],
    fill: data.datasets[0].backgroundColor?.[index] || `#${Math.floor(Math.random()*16777215).toString(16)}`
  }));

  return (
    <ResponsiveContainer width="100%" height={200}>
      <RechartsPieChart>
        <Pie
          data={transformedData}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
          animationDuration={1000}
          animationEasing="ease-out"
          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
        >
          {transformedData.map((entry: any, index: number) => (
            <Cell key={`cell-${index}`} fill={entry.fill} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </RechartsPieChart>
    </ResponsiveContainer>
  );
};
