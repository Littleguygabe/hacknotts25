import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"

interface TimeRangeButtonGroupProps {
  timeRange: string;
  setTimeRange: (timeRange: string) => void;
}

export function TimeRangeButtonGroup({ timeRange, setTimeRange }: TimeRangeButtonGroupProps) {
  return (
    <ButtonGroup>
      <Button
        variant={timeRange === "24h" ? "secondary" : "outline"}
        onClick={() => setTimeRange("24h")}
      >
        24h
      </Button>
      <Button
        variant={timeRange === "7d" ? "secondary" : "outline"}
        onClick={() => setTimeRange("7d")}
      >
        7d
      </Button>
      <Button
        variant={timeRange === "3m" ? "secondary" : "outline"}
        onClick={() => setTimeRange("3m")}
      >
        3m
      </Button>
      <Button
        variant={timeRange === "1y" ? "secondary" : "outline"}
        onClick={() => setTimeRange("1y")}
      >
        1y
      </Button>
    </ButtonGroup>
  )
}