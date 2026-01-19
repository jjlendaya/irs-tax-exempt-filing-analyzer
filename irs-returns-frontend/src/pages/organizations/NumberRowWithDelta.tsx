import { DEFAULT_NULL_VALUE } from "@/lib/constants";
import { formatCurrency } from "@/lib/utils";
import type { OrganizationReturn } from "@/types/api";
import { Delta } from "@/components/Delta";
import { NullCell } from "./NullCell";

export const NumberRowWithDelta = ({
  currentKey,
  previousKey,
  returnValue,
  isCurrency = false,
}: {
  currentKey: keyof OrganizationReturn;
  previousKey: keyof OrganizationReturn;
  returnValue: OrganizationReturn | null;
  isCurrency?: boolean;
}) => {
  if (!returnValue) {
    return <div className="text-right">{DEFAULT_NULL_VALUE}</div>;
  }

  return returnValue?.[currentKey] ? (
    <div className="flex flex-row items-center gap-2 text-right justify-end">
      {isCurrency
        ? formatCurrency(returnValue?.[currentKey])
        : returnValue?.[currentKey]}
      <Delta
        currentValue={returnValue?.[currentKey]}
        previousValue={returnValue?.[previousKey]}
        tooltipSide="right"
        isCurrency={isCurrency}
      />
    </div>
  ) : (
    <div className="flex flex-row justify-end">
      <NullCell />
    </div>
  );
};
