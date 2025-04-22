FROM node:18-alpine

WORKDIR /app

COPY package.json ./

# Install dependencies directly in Dockerfile
RUN npm install && \
    npm install --save \
    react-router-dom@6.2.1 \
    react-icons@4.3.1 \
    react-chartjs-2@4.0.1 \
    chart.js@3.7.1 \
    axios@0.26.0

COPY . .

EXPOSE 3000

# Simple direct command instead of using startup.sh
CMD npm start