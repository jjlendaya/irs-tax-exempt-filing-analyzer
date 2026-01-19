import type { ColumnDef } from "@tanstack/react-table";
import { ArrowUpDown } from "lucide-react";
import { Link } from "@tanstack/react-router";
import type { Company } from "@/types/api";
import { Button } from "@/components/ui/button";
import { formatCurrency, formatDate } from "@/lib/utils";

export const columns: ColumnDef<Company>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Organization Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
    cell: ({ row }) => {
      const company = row.original;
      return (
        <Link
          to="/companies/$companyId"
          params={{ companyId: company.id }}
          className="font-medium hover:underline"
        >
          {company.name}
        </Link>
      );
    },
  },
  {
    id: "latestFiling",
    header: "Latest Filing",
    cell: ({ row }) => {
      const returns = row.original.returns;
      if (!returns || returns.length === 0) {
        return <span className="text-muted-foreground">No filings</span>;
      }

      // Get most recent return
      const latest = returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      );

      return <span>{formatDate(latest.filedOn)}</span>;
    },
  },
  {
    id: "websiteUrl",
    header: "Website",
    cell: ({ row }) => {
      const company = row.original;
      return (
        <a href={company.websiteUrl} target="_blank" rel="noopener noreferrer">
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
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Revenue
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
    cell: ({ row }) => {
      const returns = row.original.returns;
      if (!returns || returns.length === 0) return "N/A";

      const latest = returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      );

      return (
        <div className="text-right">{formatCurrency(latest.totalRevenue)}</div>
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
    header: "Expenses",
    cell: ({ row }) => {
      const returns = row.original.returns;
      if (!returns || returns.length === 0) return "N/A";

      const latest = returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      );

      return (
        <div className="text-right">{formatCurrency(latest.totalExpenses)}</div>
      );
    },
  },
  {
    id: "totalAssetsEoy",
    header: "Assets",
    cell: ({ row }) => {
      const returns = row.original.returns;
      if (!returns || returns.length === 0) return "N/A";

      const latest = returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      );

      return (
        <div className="text-right">
          {formatCurrency(latest.totalAssetsEoy)}
        </div>
      );
    },
  },
  {
    id: "employeeCount",
    header: "Employees",
    cell: ({ row }) => {
      const returns = row.original.returns;
      if (!returns || returns.length === 0) return "N/A";

      const latest = returns.reduce((prev, current) =>
        new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
      );

      return <div className="text-center">{latest.employeeCount ?? "N/A"}</div>;
    },
  },
];
