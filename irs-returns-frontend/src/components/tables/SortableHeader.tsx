import { useCallback } from "react";
import { SortArrow } from "../SortArrow";
import { Button } from "../ui/button";
import type { Column } from "@tanstack/react-table";
import { cn } from "@/lib/utils";

interface Props<T> {
  column: Column<T>;
  children: React.ReactNode;
  className?: string;
}

export const SortableHeader = <T,>({
  column,
  children,
  className,
}: Props<T>) => {
  const handleSort = useCallback(() => {
    if (column.getIsSorted() == "asc") {
      column.toggleSorting(true);
    } else if (column.getIsSorted() == "desc") {
      column.clearSorting();
    } else {
      column.toggleSorting(false);
    }
  }, [column]);

  return (
    <div className={cn("flex items-center gap-2", className)}>
      {children}
      <Button variant="ghost" onClick={handleSort} size="icon-sm">
        <SortArrow sorting={column.getIsSorted()} />
      </Button>
    </div>
  );
};
