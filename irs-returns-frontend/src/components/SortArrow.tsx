import type { SortDirection } from "@tanstack/react-table";
import { ArrowUp, ArrowDown, ArrowUpDown } from "lucide-react";

interface Props {
  sorting: SortDirection | false;
}

export const SortArrow = ({ sorting }: Props) => {
  if (sorting === "asc") {
    return <ArrowUp className="h-4 w-4" />;
  }
  if (sorting === "desc") {
    return <ArrowDown className="h-4 w-4" />;
  }
  return <ArrowUpDown className="h-4 w-4" />;
};
