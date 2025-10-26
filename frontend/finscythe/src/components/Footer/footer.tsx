import React from 'react';

export function Footer() {
  return (
    <footer className="bg-card text-card-foreground p-4 text-center mt-8">
      <p>&copy; {new Date().getFullYear()} FinScythe. All rights reserved.</p>
    </footer>
  );
}
