import type { ColumnDef } from "@tanstack/react-table";
import { Link } from "@tanstack/react-router";
import type { Company } from "@/types/api";
import { formatCurrency, formatDate } from "@/lib/utils";
import { SortableHeader } from "@/components/tables/SortableHeader";
import { compareAsc } from "date-fns";

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
          className="font-medium underline underline-offset-4"
        >
          {company.name}
        </Link>
      );
    },
  },
  {
    id: "latestFiling",
    accessorFn: (row) =>
      row.returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      ).filedOn || null,
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
      return <span>{company.missionDescription}</span>;
    },
  },
  {
    id: "totalRevenue",
    accessorFn: (row) =>
      row.returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      ).totalRevenue || "0",
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
      return (
        <div className="text-right">{formatCurrency(getValue() as string)}</div>
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
    accessorFn: (row) =>
      row.returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      ).totalExpenses || "0",
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
      return (
        <div className="text-right">{formatCurrency(getValue() as string)}</div>
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
    accessorFn: (row) =>
      row.returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      ).totalAssetsEoy || "0",
    header: ({ column }) => {
      return <SortableHeader column={column} children="End of Year Assets" />;
    },
    cell: ({ getValue }) => {
      return (
        <div className="text-right">{formatCurrency(getValue() as string)}</div>
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
    accessorFn: (row) =>
      row.returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      ).employeeCount ?? 0,
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
      return (
        <div className="text-center">
          {(getValue() as number | null) ?? "N/A"}
        </div>
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
