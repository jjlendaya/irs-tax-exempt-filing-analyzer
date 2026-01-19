import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export const NullCell = () => {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Badge variant="noData" className="cursor-pointer">
          No Data
        </Badge>
      </TooltipTrigger>
      <TooltipContent side="right">
        Field data not available in this return
      </TooltipContent>
    </Tooltip>
  );
};
