import {
  Item,
  ItemContent,
  ItemDescription,
  ItemTitle,
} from "@/components/ui/item"

export function ItemFinScythe() {
  return (
    <div className="flex w-full max-w-md flex-col gap-6">
      <Item variant="outline">
        <ItemContent>
          <ItemTitle>Predictions</ItemTitle>
          <ItemDescription>
            Providing AI-driven market predictions.
          </ItemDescription>
        </ItemContent>
      </Item>
    </div>
  )
}