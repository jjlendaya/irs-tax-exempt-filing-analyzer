import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  beforeLoad: async () => {
    throw Route.redirect({ to: "/companies" });
  },
});
