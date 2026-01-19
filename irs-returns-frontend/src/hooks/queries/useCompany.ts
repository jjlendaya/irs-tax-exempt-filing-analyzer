import { useQuery } from "@tanstack/react-query";
import { getCompany } from "@/lib/api/companies";

export const useCompany = (id: string) => {
  return useQuery({
    queryKey: ["companies", id],
    queryFn: () => getCompany(id),
    enabled: !!id,
  });
};
