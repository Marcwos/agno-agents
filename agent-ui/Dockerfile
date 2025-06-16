FROM node:18 AS builder

RUN npm install -g pnpm

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .
RUN pnpm run build

FROM node:18-alpine AS runner

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --prod

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./next.config.js
COPY --from=builder /app/next.config.ts ./next.config.ts

# Variable de entorno del puerto
ENV PORT=8080
EXPOSE 8080

CMD ["pnpm", "start"]
