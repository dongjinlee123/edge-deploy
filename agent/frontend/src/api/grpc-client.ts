/**
 * gRPC-Web channel configuration.
 *
 * The Envoy proxy (port 8080) translates gRPC-Web ↔ gRPC and routes to
 * the controller on port 50051.
 *
 * In development:  set VITE_GRPC_HOST=http://localhost:8080
 * In production:   Envoy runs alongside the frontend; same origin, port 8080.
 */

import './protobuf-polyfill'

// Vite replaces import.meta.env at build time.
export const GRPC_HOST: string =
  (import.meta.env.VITE_GRPC_HOST as string | undefined) ?? 'http://localhost:8001'
