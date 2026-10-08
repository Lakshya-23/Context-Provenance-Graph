import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  // Ensure no /backend routes are accessible via browser
  async redirects() {
    return [
      {
        source: "/backend",
        destination: "/",
        permanent: false,
      },
      {
        source: "/backend/:path*",
        destination: "/",
        permanent: false,
      },
    ];
  },
};

export default nextConfig;
