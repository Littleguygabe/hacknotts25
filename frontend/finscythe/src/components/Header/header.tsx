'use client'

import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { SearchStock } from './SearchStock';

export function Header() {

  return (
    <div className="bg-card text-card-foreground p-4 flex items-center justify-between">
      {/* Group for left-aligned items: Home and Stocks */}
      <div className="flex gap-4"> 
        <Link to="/">
          <Button variant="ghost">Home</Button>
        </Link>
        <Link to="/discovery">
          <Button variant="ghost">Discovery</Button>
        </Link>
      </div>
      <SearchStock />
    </div>
  )
}