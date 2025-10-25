'use client'

import * as React from "react"
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"

import { StockLogo } from './StockLogo'
import appleLogo from '@/assets/applelogo.jpg'
import StockTitle from './stock-title'

import {
  Card,
  CardContent,
  CardHeader,
} from "@/components/ui/card"
import type { ChartConfig } from "@/components/ui/chart"
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { TimeRangeButtonGroup } from './TimeRangeButtonGroup'

export const description = "An interactive area chart with date and time"

// Generate data for the last 100 days, with hourly data for the last day
const generateChartData = () => {
  const data = [];
  const today = new Date();

  // Generate hourly data for the last 24 hours
  for (let i = 0; i < 24; i++) {
    const date = new Date(today);
    date.setHours(today.getHours() - i);
    data.push({
      timestamp: date.toISOString(),
      desktop: Math.floor(Math.random() * 100) + 50,
      mobile: Math.floor(Math.random() * 100) + 50,
    });
  }

  // Generate daily data for the 99 days before that
  for (let i = 1; i < 100; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    data.push({
      timestamp: date.toISOString(),
      desktop: Math.floor(Math.random() * 500) + 50,
      mobile: Math.floor(Math.random() * 500) + 50,
    });
  }
  // Sort data chronologically
  return data.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
};

const chartData = generateChartData();

const chartConfig = {
  visitors: {
    label: "Visitors",
  },
  desktop: {
    label: "Desktop",
    color: "var(--chart-1)",
  },
  mobile: {
    label: "Mobile",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig

export function ChartAreaWithDateTime() {
  const [timeRange, setTimeRange] = React.useState("7d")

  const filteredData = chartData.filter((item) => {
    const date = new Date(item.timestamp)
    const referenceDate = new Date()
    let daysToSubtract = 0;

    switch (timeRange) {
      case "24h":
        daysToSubtract = 1;
        break;
      case "7d":
        daysToSubtract = 7;
        break;
      case "3m":
        daysToSubtract = 90;
        break;
      case "1y":
        // We only have 100 days of data, so 1y will show all of it
        daysToSubtract = 100;
        break;
      default:
        daysToSubtract = 7;
    }

    const startDate = new Date(referenceDate)
    startDate.setDate(startDate.getDate() - daysToSubtract)
    return date >= startDate
  })

  return (
    <Card className="pt-0">
      <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
        <div className="flex flex-1 items-center gap-2">
            <StockLogo image={appleLogo} />
            <StockTitle />
        </div>
        <TimeRangeButtonGroup timeRange={timeRange} setTimeRange={setTimeRange} />
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <AreaChart data={filteredData}>
            <defs>
              <linearGradient id="fillDesktop" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-desktop)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-desktop)"
                  stopOpacity={0.1}
                />
              </linearGradient>
              <linearGradient id="fillMobile" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor="var(--color-mobile)"
                  stopOpacity={0.8}
                />
                <stop
                  offset="95%"
                  stopColor="var(--color-mobile)"
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="timestamp"
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
              dataKey="mobile"
              type="natural"
              fill="url(#fillMobile)"
              stroke="var(--color-mobile)"
              stackId="a"
            />
            <Area
              dataKey="desktop"
              type="natural"
              fill="url(#fillDesktop)"
              stroke="var(--color-desktop)"
              stackId="a"
            />
            <ChartLegend content={<ChartLegendContent />} />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}