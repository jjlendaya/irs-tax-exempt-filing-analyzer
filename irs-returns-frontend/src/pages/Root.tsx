import { Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";

const Root = () => {
  return (
    <main className="min-h-screen bg-page-background">
      <Outlet />
      <TanStackRouterDevtools initialIsOpen={false} />
    </main>
  );
};

export default Root;
