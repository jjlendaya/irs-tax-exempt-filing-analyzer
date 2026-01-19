import type { ColumnDef } from "@tanstack/react-table";
import { Link } from "@tanstack/react-router";
import type { Company, OrganizationReturn } from "@/types/api";
import { formatDate } from "@/lib/utils";
import { SortableHeader } from "@/components/tables/SortableHeader";
import { compareAsc } from "date-fns";
import { DEFAULT_NULL_VALUE } from "@/lib/constants";
import { NumberRowWithDelta } from "./NumberRowWithDelta";
import { NullCell } from "./NullCell";

const getLatestReturn = (company: Company): OrganizationReturn | null => {
  if (!company.returns || company.returns.length === 0) return null;

  return company.returns.reduce((prev, current) =>
    new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
  );
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
      return <span>{formatDate(getValue() as string)}</span>;
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
          className="underline underline-offset-4"
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
      return (
        <p className="max-w-[500px] text-wrap">{company.missionDescription}</p>
      );
    },
  },
  {
    id: "totalRevenue",
    accessorFn: (row) => getLatestReturn(row),
    header: ({ column }) => {
      return (
        <SortableHeader
          column={column}
          children="Total Revenue"
          className="justify-end"
        />
      );
    },
    cell: ({ getValue }) => {
      const latestReturn = getValue() as OrganizationReturn | null;
      if (!latestReturn) {
        return <div className="text-right">{DEFAULT_NULL_VALUE}</div>;
      }

      return (
        <NumberRowWithDelta
          currentKey="totalRevenue"
          previousKey="pyTotalRevenue"
          returnValue={latestReturn}
          isCurrency
        />
      );
    },
    sortingFn: (rowA, rowB) => {
      const getLatestRevenue = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return 0;
        const latest = company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        );
        return parseFloat(latest.totalRevenue || "0");
      };

      return getLatestRevenue(rowA.original) - getLatestRevenue(rowB.original);
    },
  },
  {
    id: "totalExpenses",
    accessorFn: (row) => getLatestReturn(row),
    header: ({ column }) => {
      return (
        <SortableHeader
          column={column}
          children="Total Expenses"
          className="justify-end"
        />
      );
    },
    cell: ({ getValue }) => {
      const latestReturn = getValue() as OrganizationReturn | null;
      if (!latestReturn) {
        return <div className="text-right">{DEFAULT_NULL_VALUE}</div>;
      }

      return (
        <NumberRowWithDelta
          currentKey="totalExpenses"
          previousKey="pyTotalExpenses"
          returnValue={latestReturn}
          isCurrency
        />
      );
    },
    sortingFn: (rowA, rowB) => {
      const getLatestExpenses = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return 0;
        const latest = company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        );
        return parseFloat(latest.totalExpenses || "0");
      };

      return (
        getLatestExpenses(rowA.original) - getLatestExpenses(rowB.original)
      );
    },
  },
  {
    id: "totalAssetsEoy",
    accessorFn: (row) => getLatestReturn(row),
    header: ({ column }) => {
      return <SortableHeader column={column} children="End of Year Assets" />;
    },
    cell: ({ getValue }) => {
      const latestReturn = getValue() as OrganizationReturn | null;
      if (!latestReturn) {
        return <div className="text-right">{DEFAULT_NULL_VALUE}</div>;
      }

      return (
        <NumberRowWithDelta
          currentKey="totalAssetsEoy"
          previousKey="totalAssetsBoy"
          returnValue={latestReturn}
          isCurrency
        />
      );
    },
    sortingFn: (rowA, rowB) => {
      const getLatestAssetsEoy = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return 0;
        const latest = company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        );
        return parseFloat(latest.totalAssetsEoy || "0");
      };

      return (
        getLatestAssetsEoy(rowA.original) - getLatestAssetsEoy(rowB.original)
      );
    },
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
    cell: ({ getValue }) => {
      const latestReturn = getValue() as OrganizationReturn | null;
      if (!latestReturn) {
        return (
          <div className="flex flex-row justify-end">{DEFAULT_NULL_VALUE}</div>
        );
      }

      return (
        <NumberRowWithDelta
          currentKey="employeeCount"
          previousKey="pyEmployeeCount"
          returnValue={latestReturn}
        />
      );
    },
    sortingFn: (rowA, rowB) => {
      const getLatestEmployeeCount = (company: Company) => {
        if (!company.returns || company.returns.length === 0) return 0;
        const latest = company.returns.reduce((prev, current) =>
          new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
        );
        return latest.employeeCount ?? 0;
      };

      return (
        getLatestEmployeeCount(rowA.original) -
        getLatestEmployeeCount(rowB.original)
      );
    },
  },
];
