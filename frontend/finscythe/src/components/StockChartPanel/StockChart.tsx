'use client'

import * as React from "react"
import { useMemo } from "react"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"

import { StockLogo } from './StockLogo'
import StockTitle from './stock-title'
import { PercentageChange } from './PercentageChange'

import {
  Card,
  CardContent,
  CardHeader,
} from "@/components/ui/card"
import type { ChartConfig } from "@/components/ui/chart"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { TimeRangeButtonGroup } from './TimeRangeButtonGroup'

const chartConfig = {
  price: {
    label: "Price",
    color: "#22c55e", // Changed to green
  },
} satisfies ChartConfig

const convertTimeRangeToDays = (timeRange: string) => {
  switch (timeRange) {
    case "24h":
      return 1;
    case "7d":
      return 7;
    case "3m":
      return 90;
    case "1y":
      return 365;
    default:
      return 7;
  }
}

export function ChartAreaWithDateTime({ ticker }: { ticker: string }) {
  const [timeRange, setTimeRange] = React.useState("24h");
  const [chartData, setChartData] = React.useState<{ Datetime: string; Close: number }[]>([]); 
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchStockData = async () => {
      setIsLoading(true);
      try {
        const days = convertTimeRangeToDays(timeRange);
        const response = await fetch(`http://127.0.0.1:8000/stock/${ticker}?time_period=${days}`);
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
                        let tickerHistory = Array.isArray(data.ticker_history) ? data.ticker_history : [];

        if (timeRange === '1y') {
          const oneYearAgo = new Date();
          oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);

          tickerHistory = tickerHistory.filter((d: { Datetime: string }) => new Date(d.Datetime) >= oneYearAgo);
        }
        
        interface StockDataPoint {
  Datetime: string;
  Close: number;
}

// ... (keep existing code)

        // This ensures the data is correctly typed as numbers.
        const processedData = tickerHistory.map((d: StockDataPoint) => ({
          Datetime: d.Datetime,
          Close: Number(d.Close), 
        }));
        
        setChartData(processedData);
        
      } catch (error) {
        console.error('Failed to fetch stock data:', error);
        setChartData([]); 
      } finally {
        setIsLoading(false);
      }
    };

    fetchStockData();
  }, [timeRange, ticker]);

  const yAxisDomain = useMemo(() => {
    const prices = chartData.map(d => d.Close).filter(p => !isNaN(p));
    
    if (prices.length < 2) {
      return ['auto', 'auto'];
    }

    const min = Math.min(...prices);
    const max = Math.max(...prices);

    if (min === max) {
      // If all prices are the same, create a small range around the price.
      const padding = min * 0.005; // Use a very small padding for flat data
      return [min - padding, max + padding];
    }

    const priceRange = max - min;
    const padding = priceRange * 0.1; // 10% padding

    const domainStart = min - padding;
    
    // Ensures the bottom of the axis is either the calculated start or 0, whichever is greater.
    return [Math.max(0, domainStart), max + padding];
  }, [chartData]);

    const mostRecentPrice = chartData.length > 0 ? chartData[chartData.length - 1].Close : null;

  const firstDataPoint = chartData.length > 0 ? chartData[0] : null;
  const lastDataPoint = chartData.length > 0 ? chartData[chartData.length - 1] : null;

  let percentageChange = null;
  if (firstDataPoint && lastDataPoint && firstDataPoint.Close !== 0) {
    percentageChange = ((lastDataPoint.Close - firstDataPoint.Close) / firstDataPoint.Close) * 100;
  }

  return (
    <Card className="pt-0">
      <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
        <div className="flex flex-1 items-center gap-2">
          <StockLogo ticker={ticker} />
                    <StockTitle ticker={ticker} price={mostRecentPrice} />
          <PercentageChange percentageChange={percentageChange} />
        </div>
        <TimeRangeButtonGroup timeRange={timeRange} setTimeRange={setTimeRange} />
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[350px] w-full"
        >
          {isLoading ? (
            <div className="flex h-full w-full items-center justify-center">Loading...</div>
          ) : (
            <AreaChart data={chartData} margin={{ left: 12, right: 12 }}>
              <defs>
                <linearGradient id="fillPrice" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="var(--color-price)"
                    stopOpacity={0.8}
                  />
                  <stop
                    offset="95%"
                    stopColor="var(--color-price)"
                    stopOpacity={0.1}
                  />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="Datetime"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                minTickGap={32}
                tickFormatter={(value) => {
                  const date = new Date(value)
                  if (timeRange === '24h') {
                    return date.toLocaleTimeString("en-US", {
                      hour: 'numeric',
                      minute: '2-digit'
                    });
                  }
                  return date.toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                  })
                }}
              />
              <YAxis 
                domain={yAxisDomain} 
                tickFormatter={(value) => `$${value.toFixed(2)}`}
              />
              <ChartTooltip
                cursor={false}
                content={
                  <ChartTooltipContent
                    labelFormatter={(value: string) => {
                      return new Date(value).toLocaleString("en-US", {
                        dateStyle: "medium",
                        timeStyle: "short",
                      })
                    }}
                    indicator="dot"
                  />
                }
              />
              <Area
                dataKey="Close"
                type="natural"
                fill="url(#fillPrice)"
                stroke="var(--color-price)"
                // 🛑 SOLUTION: Remove stackId="a" to prevent the Y-axis from being forced to start at 0
                // stackId="a" 
              />
            </AreaChart>
          )}
        </ChartContainer>
      </CardContent>
    </Card>
  )
}