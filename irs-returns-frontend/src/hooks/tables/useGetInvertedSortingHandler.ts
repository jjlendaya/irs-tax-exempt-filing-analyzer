import type { Column } from "@tanstack/react-table";

export const useGetInvertedSortingHandler = <T>({
  column,
}: {
  column: Column<T>;
}) => {
  // Tanstack's default behavior is: no sort -> descending sort -> ascending sort.
  // We want to invert this behavior so that: no sort -> ascending sort -> descending sort.
  const handleSort = () => {
    if (column.getIsSorted() == "asc") {
      column.toggleSorting(true);
    } else if (column.getIsSorted() == "desc") {
      column.clearSorting();
    } else {
      column.toggleSorting(false);
    }
  };

  return { handleSort };
};
