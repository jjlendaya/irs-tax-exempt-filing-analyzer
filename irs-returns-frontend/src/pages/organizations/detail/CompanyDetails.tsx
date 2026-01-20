import { useCompany } from "@/hooks/queries/useCompany";
import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency, formatDate } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ArrowLeftIcon, ExternalLinkIcon, InfoIcon } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Badge } from "@/components/ui/badge";
import { DEFAULT_EMPTY_VALUE } from "@/lib/constants";
import { Delta } from "@/components/Delta";
import { Link } from "@tanstack/react-router";

const InfoCard = ({
  title,
  displayValue,
  currentValue,
  previousValue,
  isCurrency = false,
}: {
  title: string;
  displayValue: string | null;
  currentValue: string | null;
  previousValue?: string | null;
  isCurrency?: boolean;
}) => {
  return (
    <Card className="w-full p-0">
      <CardContent className="flex flex-col justify-between h-full p-4 gap-4">
        <h2 className="font-bold text-muted-foreground uppercase text-xs tracking-wider">
          {title}
        </h2>
        <p className="text-2xl font-bold">
          {displayValue || DEFAULT_EMPTY_VALUE}
        </p>
        <Delta
          currentValue={currentValue}
          previousValue={previousValue}
          isCurrency={isCurrency}
        />
      </CardContent>
    </Card>
  );
};

export const CompanyDetails = ({ companyId }: { companyId: string }) => {
  const { data: company, isLoading, isError, error } = useCompany(companyId);
  if (isLoading) {
    return (
      <div className="container mx-auto py-10">
        <Skeleton className="h-12 w-[300px]" />
      </div>
    );
  }
  if (isError && error && "message" in error) {
    return (
      <div className="container mx-auto py-10">
        <Card>
          <CardHeader>
            <CardTitle>Error: {error.message}</CardTitle>
          </CardHeader>
        </Card>
      </div>
    );
  }
  if (!company) {
    return (
      <div className="container mx-auto py-10">
        <Card>
          <CardHeader>
            <CardTitle>Company not found</CardTitle>
          </CardHeader>
        </Card>
      </div>
    );
  }

  const latestReturn = company.returns.reduce((prev, current) =>
    new Date(current.filedOn) > new Date(prev.filedOn) ? current : prev
  );

  const totalExpenses = parseFloat(latestReturn.totalExpenses || "0");
  const totalRevenue = parseFloat(latestReturn.totalRevenue || "0");
  const profitStatus: "profitable" | "scaling" | "neutral" =
    totalRevenue > totalExpenses
      ? "profitable"
      : totalRevenue < totalExpenses
        ? "scaling"
        : "neutral";

  return (
    <main className="container mx-auto py-10 px-10 md:px-0">
      <div className="flex flex-col gap-8">
        <Button variant="outline" asChild className="w-fit">
          <Link to="/companies" className="flex flex-row items-center gap-2">
            <ArrowLeftIcon /> Back to Companies
          </Link>
        </Button>
        <Card>
          <CardContent className="flex flex-col gap-4">
            <div className="flex flex-row items-center justify-between w-full">
              <div>
                <div className="flex flex-col gap-2">
                  <h1 className="text-3xl font-bold tracking-tight">
                    {company.name}
                  </h1>
                  <div className="flex flex-row items-center gap-2">
                    <Tooltip>
                      <TooltipTrigger className="cursor-pointer">
                        <Badge
                          variant={
                            profitStatus === "profitable"
                              ? "success"
                              : profitStatus === "scaling"
                                ? "warning"
                                : "info"
                          }
                        >
                          {profitStatus === "profitable"
                            ? "Profitable"
                            : profitStatus === "scaling"
                              ? "Scaling"
                              : "Neutral"}
                        </Badge>
                      </TooltipTrigger>
                      <TooltipContent>
                        {profitStatus === "profitable"
                          ? "Profitable companies have higher revenue than expenses."
                          : profitStatus === "scaling"
                            ? "Scaling companies have higher expenses than revenue."
                            : "Companies with equal revenue and expenses are neither profitable nor scaling."}
                      </TooltipContent>
                    </Tooltip>
                  </div>
                </div>
                <div>
                  <p className="mt-2">{company.missionDescription}</p>
                </div>
              </div>
              <div>
                {company.websiteUrl ? (
                  <Tooltip>
                    <TooltipTrigger>
                      <Button variant="outline" asChild>
                        <a
                          href={company.websiteUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Visit Webpage <ExternalLinkIcon />
                        </a>
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>{company.websiteUrl}</TooltipContent>
                  </Tooltip>
                ) : (
                  <Tooltip>
                    <TooltipTrigger>
                      <Button variant="outline" disabled>
                        Visit Webpage <ExternalLinkIcon />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      No website available from latest return.
                    </TooltipContent>
                  </Tooltip>
                )}
              </div>
            </div>
            <div className="flex flex-row items-center gap-2 text-muted-foreground text-sm">
              <InfoIcon className="size-4" />
              <span>
                Information is based on the latest return for the tax period{" "}
                <span className="font-bold">
                  {formatDate(latestReturn.taxPeriodStartDate)} -{" "}
                  {formatDate(latestReturn.taxPeriodEndDate)}.
                </span>
              </span>
            </div>
          </CardContent>
        </Card>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-stretch gap-4">
          <InfoCard
            title="Total Revenue"
            displayValue={formatCurrency(latestReturn.totalRevenue || "0")}
            currentValue={latestReturn.totalRevenue || null}
            previousValue={latestReturn.pyTotalRevenue || null}
            isCurrency
          />
          <InfoCard
            title="Total Expenses"
            displayValue={formatCurrency(latestReturn.totalExpenses || "0")}
            currentValue={latestReturn.totalExpenses || null}
            previousValue={latestReturn.pyTotalExpenses || null}
            isCurrency
          />
          <InfoCard
            title="End of Year Assets"
            displayValue={formatCurrency(latestReturn.totalAssetsEoy || "0")}
            currentValue={latestReturn.totalAssetsEoy || null}
            previousValue={latestReturn.totalAssetsBoy || null}
            isCurrency
          />
          <InfoCard
            title="Employee Count"
            displayValue={latestReturn.employeeCount?.toString() || null}
            currentValue={latestReturn.employeeCount?.toString() || null}
          />
        </div>
      </div>
    </main>
  );
};
