import { useQuery } from "@tanstack/react-query";
import { getCompanies, type GetCompaniesParams } from "@/lib/api/companies";

export const useCompanies = (params?: GetCompaniesParams) => {
  return useQuery({
    queryKey: ["companies", params],
    queryFn: () => getCompanies(params),
    staleTime: 1000 * 60 * 5,
  });
};
