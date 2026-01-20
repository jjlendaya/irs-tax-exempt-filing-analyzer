import { getCompany } from "@/lib/api/companies";
import { queryClient } from "@/lib/queryClient";
import { CompanyDetails } from "@/pages/organizations/detail/CompanyDetails";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/companies/$companyId")({
  beforeLoad: async () => {
    document.title = `IRS Returns - Company Details`;
  },
  loader: async ({ params }) => {
    const { companyId } = params;
    await queryClient.ensureQueryData({
      queryKey: ["companies", companyId],
      queryFn: () => getCompany(companyId),
    });
    return { companyId };
  },
  component: RouteComponent,
});

function RouteComponent() {
  const { companyId } = Route.useParams();
  return <CompanyDetails companyId={companyId} />;
}
