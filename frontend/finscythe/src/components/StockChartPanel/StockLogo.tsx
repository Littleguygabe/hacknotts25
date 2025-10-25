import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "@/components/ui/avatar"
  
  interface StockLogoProps {
    ticker: string;
  }
  
  export function StockLogo({ ticker }: StockLogoProps) {
    return (
      <div className="flex flex-row flex-wrap items-center gap-2">
        <Avatar>
          <AvatarImage src={`https://financialmodelingprep.com/image-factory-v2/company-logo/${ticker}.png`} alt={`${ticker} Logo`} />
          <AvatarFallback>{ticker}</AvatarFallback>
        </Avatar>
        </div>
    )
  }