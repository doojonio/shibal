FROM node:lts-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install -g @angular/cli

RUN npm install

COPY . .

RUN npm run build --prod

FROM nginx:1.27.4

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist/shibal/browser /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
