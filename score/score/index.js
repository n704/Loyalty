const express = require('express')
const app = express()
const port = 8080
// const sqlite3 = require('sqlite3').verbose();

var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

app.post('/reduce_bonus_points', (req, res) => {
  console.log(req.headers)
  let http_header_key = req.headers.score_key
  console.log("process")
  console.log(process.env.API_KEY)
  if (http_header_key == process.env.API_KEY) {
    console.log("Updated")
    var sqlite3 = require('sqlite3').verbose()
    let db = new sqlite3.Database('/db.sqlite3', (err) => {
      if (err) {
        console.error(err.message);
      }
      var { user_id , value } = req.body
      var sql_get = 'SELECT * from booking_bookinguser where id = ?'
      db.get(sql_get, [ user_id], ( err, row) => {
        if (err) {
          console.error(err)
        }
        let new_value = row.bonus_point - value
        console.log(new_value, row.bonus_point, value)
        var sql = `UPDATE booking_bookinguser SET bonus_point = ? where id= ?`
        db.run(sql,[ new_value, user_id], err => {
          if (err) {
            console.error(err.message);
          }
          console.log("Updated")
          db.close()
          res.end()
        })
      })
    });
  } else {
    console.log("Nort ssame")
    res.status(400)
  }

})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
