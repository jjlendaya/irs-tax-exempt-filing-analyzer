import api from "./client";
import type { Company, CompaniesResponse } from "@/types/api";

export interface GetCompaniesParams {
  page?: number;
  page_size?: number;
  search?: string;
  ordering?: string;
}

// Get all companies (or paginated)
export const getCompanies = async (params?: GetCompaniesParams) => {
  const { data } = await api.get<CompaniesResponse>("/companies/", { params });
  return data;
};

// Get single company by ID
export const getCompany = async (id: string) => {
  const { data } = await api.get<Company>(`/companies/${id}/`);
  return data;
};
