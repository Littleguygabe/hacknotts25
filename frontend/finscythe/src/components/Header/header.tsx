'use client'

import { Button } from "@/components/ui/button"
import { SearchStock } from "./SearchStock"

export function NavigationMenuDemo() {

  return (
    <div className="bg-card text-card-foreground p-4 flex items-center justify-between">
      {/* Group for left-aligned items: Home and Stocks */}
      <div className="flex gap-4"> 
        <Button variant="ghost">Home</Button>
        <Button variant="ghost">Stocks</Button>
      </div>
      
      {/* Search component for right-aligned item */}
      <SearchStock />
    </div>
  )
}