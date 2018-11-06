const express = require('express')
const app = express()
const port = 3000

app.use(express.static('public'))

// get port number from enviromne
// process.env.PORT

app.listen(port, () => console.log(`app running at http://localhost:${port}`))