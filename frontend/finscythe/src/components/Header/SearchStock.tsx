"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

export const tickers = [
  {
    value: "AAPL",
    label: "AAPL",
  },
  {
    value: "ABBV",
    label: "ABBV",
  },
  {
    value: "ABT",
    label: "ABT",
  },
  {
    value: "ACN",
    label: "ACN",
  },
  {
    value: "ADBE",
    label: "ADBE",
  },
  {
    value: "ADI",
    label: "ADI",
  },
  {
    value: "ADP",
    label: "ADP",
  },
  {
    value: "AMD",
    label: "AMD",
  },
  {
    value: "AMGN",
    label: "AMGN",
  },
  {
    value: "AMT",
    label: "AMT",
  },
  {
    value: "AMZN",
    label: "AMZN",
  },
  {
    value: "ANET",
    label: "ANET",
  },
  {
    value: "AON",
    label: "AON",
  },
  {
    value: "APH",
    label: "APH",
  },
  {
    value: "APD",
    label: "APD",
  },
  {
    value: "APO",
    label: "APO",
  },
  {
    value: "AVGO",
    label: "AVGO",
  },
  {
    value: "AXP",
    label: "AXP",
  },
  {
    value: "BA",
    label: "BA",
  },
  {
    value: "BAC",
    label: "BAC",
  },
  {
    value: "BK",
    label: "BK",
  },
  {
    value: "BKNG",
    label: "BKNG",
  },
  {
    value: "BLK",
    label: "BLK",
  },
  {
    value: "BMY",
    label: "BMY",
  },
  {
    value: "BRK.B",
    label: "BRK.B",
  },
  {
    value: "BSX",
    label: "BSX",
  },
  {
    value: "C",
    label: "C",
  },
  {
    value: "CAT",
    label: "CAT",
  },
  {
    value: "CB",
    label: "CB",
  },
  {
    value: "CDNS",
    label: "CDNS",
  },
  {
    value: "CEG",
    label: "CEG",
  },
  {
    value: "CI",
    label: "CI",
  },
  {
    value: "CME",
    label: "CME",
  },
  {
    value: "CMG",
    label: "CMG",
  },
  {
    value: "CMCSA",
    label: "CMCSA",
  },
  {
    value: "COF",
    label: "COF",
  },
  {
    value: "COP",
    label: "COP",
  },
  {
    value: "COST",
    label: "COST",
  },
  {
    value: "CRM",
    label: "CRM",
  },
  {
    value: "CSCO",
    label: "CSCO",
  },
  {
    value: "CVS",
    label: "CVS",
  },
  {
    value: "CVX",
    label: "CVX",
  },
  {
    value: "DHR",
    label: "DHR",
  },
  {
    value: "DE",
    label: "DE",
  },
  {
    value: "DIS",
    label: "DIS",
  },
  {
    value: "DUK",
    label: "DUK",
  },
  {
    value: "ECL",
    label: "ECL",
  },
  {
    value: "ELV",
    label: "ELV",
  },
  {
    value: "EMR",
    label: "EMR",
  },
  {
    value: "EQIX",
    label: "EQIX",
  },
  {
    value: "EXC",
    label: "EXC",
  },
  {
    value: "F",
    label: "F",
  },
  {
    value: "FI",
    label: "FI",
  },
  {
    value: "GD",
    label: "GD",
  },
  {
    value: "GE",
    label: "GE",
  },
  {
    value: "GILD",
    label: "GILD",
  },
  {
    value: "GOOG",
    label: "GOOG",
  },
  {
    value: "GOOGL",
    label: "GOOGL",
  },
  {
    value: "GS",
    label: "GS",
  },
  {
    value: "HD",
    label: "HD",
  },
  {
    value: "HON",
    label: "HON",
  },
  {
    value: "IBM",
    label: "IBM",
  },
  {
    value: "INTC",
    label: "INTC",
  },
  {
    value: "INTU",
    label: "INTU",
  },
  {
    value: "ISRG",
    label: "ISRG",
  },
  {
    value: "JCI",
    label: "JCI",
  },
  {
    value: "JNJ",
    label: "JNJ",
  },
  {
    value: "JPM",
    label: "JPM",
  },
  {
    value: "KO",
    label: "KO",
  },
  {
    value: "LIN",
    label: "LIN",
  },
  {
    value: "LLY",
    label: "LLY",
  },
  {
    value: "LMT",
    label: "LMT",
  },
  {
    value: "LOW",
    label: "LOW",
  },
  {
    value: "LRCX",
    label: "LRCX",
  },
  {
    value: "MA",
    label: "MA",
  },
  {
    value: "MCD",
    label: "MCD",
  },
  {
    value: "MDT",
    label: "MDT",
  },
  {
    value: "META",
    label: "META",
  },
  {
    value: "MMM",
    label: "MMM",
  },
  {
    value: "MMC",
    label: "MMC",
  },
  {
    value: "MO",
    label: "MO",
  },
  {
    value: "MRK",
    label: "MRK",
  },
  {
    value: "MS",
    label: "MS",
  },
  {
    value: "MSFT",
    label: "MSFT",
  },
  {
    value: "MU",
    label: "MU",
  },
  {
    value: "NEE",
    label: "NEE",
  },
  {
    value: "NFLX",
    label: "NFLX",
  },
  {
    value: "NKE",
    label: "NKE",
  },
  {
    value: "NOW",
    label: "NOW",
  },
  {
    value: "NVDA",
    label: "NVDA",
  },
  {
    value: "ORCL",
    label: "ORCL",
  },
  {
    value: "PFE",
    label: "PFE",
  },
  {
    value: "PG",
    label: "PG",
  },
  {
    value: "PH",
    label: "PH",
  },
  {
    value: "PM",
    label: "PM",
  },
  {
    value: "PNC",
    label: "PNC",
  },
  {
    value: "PYPL",
    label: "PYPL",
  },
  {
    value: "QCOM",
    label: "QCOM",
  },
  {
    value: "REGN",
    label: "REGN",
  },
  {
    value: "ROP",
    label: "ROP",
  },
  {
    value: "RTX",
    label: "RTX",
  },
  {
    value: "SBUX",
    label: "SBUX",
  },
  {
    value: "SCHW",
    label: "SCHW",
  },
  {
    value: "SO",
    label: "SO",
  },
  {
    value: "SPGI",
    label: "SPGI",
  },
  {
    value: "SYK",
    label: "SYK",
  },
  {
    value: "T",
    label: "T",
  },
  {
    value: "TDG",
    label: "TDG",
  },
  {
    value: "TGT",
    label: "TGT",
  },
  {
    value: "TMO",
    label: "TMO",
  },
  {
    value: "TMUS",
    label: "TMUS",
  },
  {
    value: "TRV",
    label: "TRV",
  },
  {
    value: "TSLA",
    label: "TSLA",
  },
  {
    value: "TXN",
    label: "TXN",
  },
  {
    value: "UBER",
    label: "UBER",
  },
  {
    value: "UNH",
    label: "UNH",
  },
  {
    value: "UNP",
    label: "UNP",
  },
  {
    value: "UPS",
    label: "UPS",
  },
  {
    value: "V",
    label: "V",
  },
  {
    value: "VRTX",
    label: "VRTX",
  },
  {
    value: "VZ",
    label: "VZ",
  },
  {
    value: "WBA",
    label: "WBA",
  },
  {
    value: "WFC",
    label: "WFC",
  },
  {
    value: "WM",
    label: "WM",
  },
  {
    value: "WMT",
    label: "WMT",
  },
  {
    value: "XOM",
    label: "XOM",
  },
  {
    value: "ZTS",
    label: "ZTS",
  },
];

import { useTicker } from '../../context/TickerContext.tsx';
import { useNavigate } from 'react-router-dom';

export function SearchStock() {
  const [open, setOpen] = React.useState(false);
  const { selectedTicker, setSelectedTicker } = useTicker();
  const navigate = useNavigate();

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[200px] justify-between"
        >
          {selectedTicker
            ? tickers.find((ticker) => ticker.value === selectedTicker)?.label
            : "Search Stocks..."}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search stock..." className="h-9" />
          <CommandList>
            <CommandEmpty>Search More...</CommandEmpty>
            <CommandGroup>
              {tickers.map((ticker) => (
                <CommandItem
                  key={ticker.value}
                  value={ticker.value}
                  onSelect={(currentValue) => {
                    setSelectedTicker(currentValue === selectedTicker ? "" : currentValue);
                    setOpen(false);
                    navigate(`/stock/${currentValue}`);
                  }}
                >
                  {ticker.label}
                  <Check
                    className={cn(
                      "ml-auto",
                      selectedTicker === ticker.value ? "opacity-100" : "opacity-0"
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}