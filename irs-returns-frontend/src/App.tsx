import { createRouter, RouterProvider } from "@tanstack/react-router";
import { routeTree } from "./routes/routeTree.gen";
import { QueryClient } from "@tanstack/react-query";

const router = createRouter({
  routeTree,
  context: {
    queryClient: new QueryClient(),
  },
});

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
