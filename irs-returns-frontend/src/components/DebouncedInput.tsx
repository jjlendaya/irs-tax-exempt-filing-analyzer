import { debounce } from "lodash";
import { Input } from "./ui/input";
import { useEffect, useState } from "react";

export const DebouncedInput = ({
  value,
  onChange,
  delay = 500,
  ...props
}: {
  value: string;
  onChange: (value: string) => void;
  delay?: number;
} & Omit<React.ComponentProps<typeof Input>, "value" | "onChange">) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    debounce(onChange, delay)(debouncedValue);
  }, [debouncedValue, onChange, delay]);

  return (
    <Input
      value={debouncedValue}
      onChange={(e) => setDebouncedValue(e.target.value)}
      {...props}
    />
  );
};
