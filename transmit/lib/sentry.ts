import * as Sentry from "@sentry/browser";

const DSN = "https://064ef0ce481bfa2769c3f10fc01fa019@o926849.ingest.us.sentry.io/4511160186503168";

let initialized = false;

export function initSentry() {
  if (initialized) return;
  Sentry.init({
    dsn: DSN,
    tracesSampleRate: 1.0,
    environment: process.env.VERCEL_ENV || "development",
  });
  initialized = true;
}

export { Sentry };
