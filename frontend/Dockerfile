FROM node:18-alpine

WORKDIR /app

COPY package.json ./

# Install dependencies explicitly
RUN npm install && \
    npm install react-router-dom@6.2.1 \
    react-icons@4.3.1 \
    react-chartjs-2@4.0.1 \
    chart.js@3.7.1 \
    axios@0.26.0

# Copy the rest of the application
COPY . .

EXPOSE 3000

CMD ["npm", "start"]