import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const DEFAULT_EMPTY_VALUE = "N/A";

export function formatCurrency(value: string | number | null): string {
  if (value === null) {
    return DEFAULT_EMPTY_VALUE;
  }
  const num = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(num)) {
    return DEFAULT_EMPTY_VALUE;
  }

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num);
}

export function formatDate(dateString: string | null): string {
  if (!dateString) {
    return DEFAULT_EMPTY_VALUE;
  }
  const date = new Date(dateString);

  if (isNaN(date.getTime())) {
    return DEFAULT_EMPTY_VALUE;
  }

  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
}

export function isNumeric(value?: string | number | null): boolean {
  if (value === null || value === undefined) {
    return false;
  }
  if (typeof value === "string") {
    return !isNaN(parseFloat(value));
  }
  if (typeof value === "number") {
    return !isNaN(value);
  }
  return false;
}

export function calculateDelta(
  current?: string | number | null,
  previous?: string | number | null
): {
  delta: number | null;
  deltaPercentage: number | null;
} {
  if (!isNumeric(current) || !isNumeric(previous)) {
    return {
      delta: null,
      deltaPercentage: null,
    };
  }

  const curr =
    typeof current === "string" ? parseFloat(current) : (current ?? 0);
  const prev =
    typeof previous === "string" ? parseFloat(previous) : (previous ?? 0);

  const delta = curr - prev;
  const deltaPercentage = prev > 0 ? (delta / prev) * 100 : null;
  return { delta, deltaPercentage };
}
