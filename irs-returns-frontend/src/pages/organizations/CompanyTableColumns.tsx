import type { ColumnDef } from "@tanstack/react-table";
import { Link } from "@tanstack/react-router";
import type { Company, OrganizationReturn } from "@/types/api";
import { formatDate } from "@/lib/utils";
import { SortableHeader } from "@/components/tables/SortableHeader";
import { compareAsc } from "date-fns";
import { NumberRowWithDelta } from "./NumberRowWithDelta";
import { NullCell } from "./NullCell";
import { InfoIcon } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const getLatestReturn = (company: Company): OrganizationReturn | undefined => {
  if (!company.returns || company.returns.length === 0) return undefined;

  return company.returns.reduce((prev, current) =>
    new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
  );
};

const getNullableSortValue = (a: number | null, b: number | null) => {
  if (a === null && b === null) return 0;
  if (a === null) return 1;
  if (b === null) return -1;
  return a - b;
};

type NumericStringKeys<T> = {
  [K in keyof T]: T[K] extends string | null ? K : never;
}[keyof T];

const getNumericValueFromLatestReturn = <
  K extends NumericStringKeys<OrganizationReturn>,
>(
  company: Company,
  key: K
) => {
  if (!company.returns || company.returns.length === 0) {
    return null;
  }
  const latest = company.returns.reduce((prev, current) =>
    new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
  );

  if (
    latest[key] === null ||
    latest[key] === undefined ||
    isNaN(parseFloat(latest[key]))
  ) {
    return null;
  }
  return parseFloat(latest[key]);
};

export const columns: ColumnDef<Company>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return <SortableHeader column={column} children="Organization Name" />;
    },
    cell: ({ row }) => {
      const company = row.original;
      return (
        <Link
          to="/companies/$companyId"
          params={{ companyId: company.id }}
          className="font-medium underline underline-offset-4 max-w-[150px] text-wrap"
        >
          {company.name}
        </Link>
      );
    },
  },
  {
    id: "latestFiling",
    accessorFn: (row) => row,
    header: ({ column }) => {
      return <SortableHeader column={column} children="Latest Filing" />;
    },
    cell: ({ getValue }) => {
      const getLatestFiling = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return null;
        return company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        ).filedOn;
      };
      return <span>{formatDate(getLatestFiling(getValue() as Company))}</span>;
    },
    sortingFn: (rowA, rowB) => {
      const getLatestFiling = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return null;
        return company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        ).filedOn;
      };

      // Use date-fns compareAsc for safer date comparison
      const aFiledOn = getLatestFiling(rowA.original);
      const bFiledOn = getLatestFiling(rowB.original);
      if (!aFiledOn && !bFiledOn) return 0;
      if (!aFiledOn) return -1;
      if (!bFiledOn) return 1;
      return compareAsc(new Date(aFiledOn), new Date(bFiledOn));
    },
  },
  {
    id: "websiteUrl",
    header: "Website",
    cell: ({ row }) => {
      const company = row.original;

      if (!company.websiteUrl) {
        return <NullCell />;
      }

      return (
        <a
          href={company.websiteUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="underline underline-offset-4 max-w-[100px] text-wrap break-all"
        >
          {company.websiteUrl}
        </a>
      );
    },
  },
  {
    id: "missionDescription",
    header: "Mission",
    cell: ({ row }) => {
      const company = row.original;
      return company.missionDescription ? (
        <p className="max-w-[500px] text-wrap">{company.missionDescription}</p>
      ) : (
        <NullCell />
      );
    },
  },
  {
    id: "totalRevenue",
    accessorFn: (row) => getLatestReturn(row)?.totalRevenue ?? undefined,
    header: ({ column }) => {
      return (
        <SortableHeader
          column={column}
          children="Total Revenue"
          className="justify-end"
        />
      );
    },
    cell: ({ row }) => {
      const latestReturn = getLatestReturn(row.original);
      return latestReturn ? (
        <NumberRowWithDelta
          currentKey="totalRevenue"
          previousKey="pyTotalRevenue"
          returnValue={latestReturn}
          isCurrency
        />
      ) : (
        <NullCell />
      );
    },
    sortingFn: (rowA, rowB) => {
      const aValue = getNumericValueFromLatestReturn(
        rowA.original,
        "totalRevenue"
      );
      const bValue = getNumericValueFromLatestReturn(
        rowB.original,
        "totalRevenue"
      );

      return getNullableSortValue(aValue, bValue);
    },
    sortUndefined: "last",
  },
  {
    id: "totalExpenses",
    accessorFn: (row) => getLatestReturn(row)?.totalExpenses ?? undefined,
    header: ({ column }) => {
      return (
        <SortableHeader
          column={column}
          children="Total Expenses"
          className="justify-end"
        />
      );
    },
    cell: ({ row }) => {
      const latestReturn = getLatestReturn(row.original);
      return latestReturn ? (
        <NumberRowWithDelta
          currentKey="totalExpenses"
          previousKey="pyTotalExpenses"
          returnValue={latestReturn}
          isCurrency
        />
      ) : (
        <NullCell />
      );
    },
    sortingFn: (rowA, rowB) => {
      const aValue = getNumericValueFromLatestReturn(
        rowA.original,
        "totalExpenses"
      );
      const bValue = getNumericValueFromLatestReturn(
        rowB.original,
        "totalExpenses"
      );

      return getNullableSortValue(aValue, bValue);
    },
    sortUndefined: "last",
  },
  {
    id: "totalAssetsEoy",
    accessorFn: (row) => getLatestReturn(row),
    header: ({ column }) => {
      return (
        <div className="flex flex-row justify-end gap-1 items-center">
          <SortableHeader
            column={column}
            children="End of Year Assets"
            className="justify-end"
          />
          <Tooltip>
            <TooltipTrigger>
              <InfoIcon className="w-4 h-4 cursor-pointer" />
            </TooltipTrigger>
            <TooltipContent side="top">
              <p>
                Note: The deltas here are with respect to the assets at the
                beginning of the year. This is not a YoY change.
              </p>
            </TooltipContent>
          </Tooltip>
        </div>
      );
    },
    cell: ({ row }) => {
      const latestReturn = getLatestReturn(row.original);
      return latestReturn ? (
        <NumberRowWithDelta
          currentKey="totalAssetsEoy"
          previousKey="totalAssetsBoy"
          returnValue={latestReturn}
          isCurrency
        />
      ) : (
        <NullCell />
      );
    },
    sortingFn: (rowA, rowB) => {
      const aValue = getNumericValueFromLatestReturn(
        rowA.original,
        "totalAssetsEoy"
      );
      const bValue = getNumericValueFromLatestReturn(
        rowB.original,
        "totalAssetsEoy"
      );

      return getNullableSortValue(aValue, bValue);
    },
    sortUndefined: "last",
  },
  {
    id: "employeeCount",
    accessorFn: (row) => getLatestReturn(row),
    header: ({ column }) => {
      return (
        <SortableHeader
          column={column}
          children="Employees"
          className="justify-end"
        />
      );
    },
    cell: ({ row }) => {
      const latestReturn = getLatestReturn(row.original);
      return latestReturn ? (
        <NumberRowWithDelta
          currentKey="employeeCount"
          previousKey="pyEmployeeCount"
          returnValue={latestReturn}
        />
      ) : (
        <NullCell />
      );
    },
    sortingFn: (rowA, rowB) => {
      const getLatestEmployeeCount = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return null;
        const latest = company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        );
        return latest.employeeCount ?? null;
      };

      const aValue = getLatestEmployeeCount(rowA.original);
      const bValue = getLatestEmployeeCount(rowB.original);
      return getNullableSortValue(aValue, bValue);
    },
    sortUndefined: "last",
  },
];
