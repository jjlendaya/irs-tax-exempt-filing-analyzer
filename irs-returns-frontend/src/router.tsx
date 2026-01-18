import { createRouter } from "@tanstack/react-router";
import { routeTree } from "./routes/routeTree.gen";
import { QueryClient } from "@tanstack/react-query";

export const router = createRouter({
  routeTree: routeTree,
  context: {
    queryClient: new QueryClient(),
  },
});
