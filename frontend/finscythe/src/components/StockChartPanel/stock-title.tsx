interface StockTitleProps {
  ticker: string;
  price: number | null;
}

function StockTitle({ ticker, price }: StockTitleProps) {
  return (
    <div className="flex items-center gap-2">
      <p className="font-bold">{ticker}</p>
      {price !== null && (
        <p className="text-gray-500">
          {price.toFixed(2)} USD
        </p>
      )}
    </div>
  );
}

export default StockTitle;