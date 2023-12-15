const swaggerDefinition = {
  openapi: '3.0.0',
  info: {
    title: 'brockai API',
    version: '1.0.0',
    description: 'LLM Processing API',
  },
  servers: [
    {
      url: 'http://localhost:3000',
      description: 'API server',
    },
  ],
};

module.exports = swaggerDefinition;
