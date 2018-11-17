FROM node:8

# Create app directory
RUN mkdir /score

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY . /score
WORKDIR /score/score
RUN npm install
# If you are building your code for production
# RUN npm install --only=production

# Bundle app source

EXPOSE 8080
CMD [ "npm", "start" ]
