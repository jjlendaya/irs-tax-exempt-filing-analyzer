import { createRootRouteWithContext } from "@tanstack/react-router";
import type { QueryClient } from "@tanstack/react-query";
import Root from "@/pages/Root";

export interface RouterContext {
  queryClient: QueryClient;
}

export const Route = createRootRouteWithContext<RouterContext>()({
  beforeLoad: async () => {
    document.title = "IRS Returns";
  },
  component: Root,
  notFoundComponent: () => <div>Not Found</div>,
});
