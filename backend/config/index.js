const path = require('path')
// require('dotenv').config({ path: path.resolve(__dirname, '../.env') })
require('dotenv').config()
module.exports = function loadConfig() {
    process.env.DOMAIN_API = process.env.DOMAIN_API,
    process.env.DOMAIN_API_SWAGGER = process.env.DOMAIN_API_SWAGGER
}
