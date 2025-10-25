import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "@/components/ui/avatar"
  
  interface StockLogoProps {
    image: string;
  }
  
  export function StockLogo({ image }: StockLogoProps) {
    return (
      <div className="flex flex-row flex-wrap items-center gap-2">
        <Avatar>
          <AvatarImage src={image} alt="Stock Logo" />
          <AvatarFallback>SL</AvatarFallback>
        </Avatar>
        </div>
    )
  }