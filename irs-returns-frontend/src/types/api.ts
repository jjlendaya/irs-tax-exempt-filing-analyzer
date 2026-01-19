/**
 * Types for the API responses.
 *
 * This file is used to type the API responses from the backend.
 *
 * Unless stated otherwise, "py_" indicates that the field is the previous year's value.
 * "eoy" indicates the end of year, "boy" indicates the beginning of year.
 */

// Base types matching your Django models
export interface OrganizationReturn {
  filedOn: string; // ISO date string
  taxPeriodStartDate: string;
  taxPeriodEndDate: string;
  employeeCount: number | null;
  pyEmployeeCount: number | null;
  totalRevenue: string | null; // Decimal as string
  pyTotalRevenue: string | null;
  totalExpenses: string | null;
  pyTotalExpenses: string | null;
  totalAssetsEoy: string | null; // End of year
  totalAssetsBoy: string | null; // Beginning of year
  totalLiabilitiesEoy: string | null;
  totalLiabilitiesBoy: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface Company {
  id: string; // UUID as string
  name: string;
  websiteUrl: string;
  missionDescription: string;
  createdAt: string;
  updatedAt: string;
  returns: OrganizationReturn[];
}

// API response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// For non-paginated responses (if needed)
export type CompaniesResponse = Company[];
