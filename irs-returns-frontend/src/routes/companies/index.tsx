import { createFileRoute } from "@tanstack/react-router";
import { CompanyTable } from "@/pages/organizations/CompanyTable";

export const Route = createFileRoute("/companies/")({
  beforeLoad: async () => {
    document.title = "IRS Returns - Companies";
  },
  component: CompaniesPage,
});

function CompaniesPage() {
  return (
    <div className="container mx-auto py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Organizations</h1>
        <p className="text-muted-foreground mt-2">
          Browse IRS tax-exempt organizations and their financial filings.
        </p>
      </div>

      <CompanyTable />
    </div>
  );
}
