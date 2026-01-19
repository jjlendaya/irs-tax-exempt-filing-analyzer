import { calculateDelta, cn, formatCurrency } from "@/lib/utils";
import { DEFAULT_NULL_VALUE } from "@/lib/constants";
import { Tooltip, TooltipContent, TooltipTrigger } from "./ui/tooltip";

export const Delta = ({
  currentValue,
  previousValue,
  isCurrency = false,
  tooltipSide = "top",
}: {
  currentValue: string | number | null;
  previousValue?: string | number | null;
  isCurrency?: boolean;
  tooltipSide?: "top" | "bottom" | "left" | "right";
}) => {
  const { delta, deltaPercentage } = calculateDelta(
    currentValue,
    previousValue
  );

  const noDelta = delta === null || delta === undefined;
  const noDeltaPercentage =
    deltaPercentage === null || deltaPercentage === undefined;

  const sign = !noDelta ? (delta > 0 ? "+" : "-") : "";

  const absoluteChange = !noDelta
    ? isCurrency
      ? formatCurrency(delta)
      : delta.toLocaleString("en-US", { maximumFractionDigits: 2 })
    : DEFAULT_NULL_VALUE;

  return (
    <div
      className={cn(
        "flex flex-row items-center gap-2 w-fit px-1 py-0.5 font-bold rounded-md",
        {
          "text-green-500 bg-green-500/10": !noDelta && delta > 0,
          "text-red-500 bg-red-500/10": !noDelta && delta < 0,
          "text-muted-foreground bg-muted-foreground/10": noDelta,
        }
      )}
    >
      <Tooltip>
        <TooltipTrigger className="cursor-pointer">
          <p className="text-xs">
            {!noDeltaPercentage
              ? `${sign}${Math.abs(deltaPercentage).toFixed(1)}%`
              : DEFAULT_NULL_VALUE}
          </p>
        </TooltipTrigger>
        <TooltipContent side={tooltipSide}>
          <p className="text-xs">
            {noDelta ? (
              <span className="font-bold">
                The company's latest or previous returns have insufficient data
                to calculate the change.
              </span>
            ) : (
              <>
                <span className="font-bold">
                  Absolute Change: {absoluteChange}
                </span>
                <br />
                <span className="font-bold">
                  Percentage Change:{" "}
                  {deltaPercentage !== null && deltaPercentage !== undefined
                    ? `${sign}${Math.abs(deltaPercentage).toFixed(1)}%`
                    : DEFAULT_NULL_VALUE}
                </span>
              </>
            )}
          </p>
        </TooltipContent>
      </Tooltip>
    </div>
  );
};
