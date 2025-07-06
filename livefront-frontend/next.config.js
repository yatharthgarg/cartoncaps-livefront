// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // turn off the in‐browser dev indicator entirely:
  devIndicators: false,

  // if you were using turbopack via `--turbopack`, you can also
  // disable it here (so you don’t have to pass --no-turbo on every run)
  experimental: {
    turbo: false,
  },
};

module.exports = nextConfig;