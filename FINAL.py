var port_name = "COM7";
var express    = require("express");
var mysql      = require('mysql');
var datos=0;
var datos1=0;
var connection= mysql.createConnection({
  host     : 'telecousta.com',
  user     : 'telecous_smuser',
  password : 'carey0810',
  database : 'telecous_test'
});
var connection1 = mysql.createConnection({
  host     : 'telecousta.com',
  user     : 'telecous_smuser',
  password : 'carey0810',
  database : 'telecous_smartmall'
});

var connection2 = mysql.createConnection({
  host     : 'telecousta.com',
  user     : 'telecous_smuser',
  password : 'carey0810',
  database : 'telecous_graficar'
});

connection.connect(function(err){
if(!err) {
    console.log("Database is connected ... nn");    
} else {
    console.log("Error connecting database ... nn"); 
 
}
});


connection1.connect(function(err){
if(!err) {
    console.log("Database is connected ... nn");    
} else {
    console.log("Error connecting database ... nn"); 
 
}
});

connection2.connect(function(err){
if(!err) {
    console.log("Database is connected ... nn");    
} else {
    console.log("Error connecting database ... nn"); 
 
}
});


if (port_name == undefined) {
    console.log("Serial port name is required.");
    process.exit(1);
}

var serial = require("serialport"),
    port = new serial.SerialPort(port_name, {
        parser: serial.parsers.readline("\r\n")
    });
console.log("Opening serial port " + port_name);

var app = require("express")(),
    server = require("http").createServer(app),
    io = require("socket.io").listen(server);

server.listen(8080);
console.log("Listening for new clients on http://localhost:8080");
var connected = false;

app.get("/", function(request, response) {
    response.sendFile(__dirname + "/client2.html");
});

io.sockets.on("connection", function(socket) {
    if (!connected) {
        port.flush();
        port.write("c");
        connected = true;
    }

    socket.on("disconnect", function() {
        port.write("x");
        connected = false;
    }).on("ledEvent", function(data) {
        port.write(data.led);
    });

/*
socket.on("disconnect", function() {
        port.write("x");
        connected = false;
    }).on("led1Event", function(data) {
        port.write(data.led);
    });
*/

    port.on("data", function(data) {
        var arr = data.split(",");
       datos= parseInt(arr[1]);
       datos1= parseInt(arr[0]);
      var serial_data = JSON.parse(datos);
/*console.log(""+arr[0]);
console.log(""+arr[1]);
console.log(""+arr[2]);*/

        socket.emit("serialEvent", serial_data);

        var info= datos;
//ir=ir+1;
//client.query("INSERT INTO graficar(id, temp) values($1, $2)", [ir, info]);

    });
});

var myvar=setInterval(myTimer,5000);


function myTimer() {



connection.query('INSERT INTO serial (dato) VALUES ('+datos+')', function(err, rows, fields) {
//connection.end();
 });


setTimeout(function() {
}, 2000);
connection2.query('INSERT INTO sensado (temp) VALUES ('+datos1+')', function(err, rows, fields) {
//connection2.end();
console.log(datos1);
 });


setTimeout(function() {
}, 1000);

connection1.query('SELECT luzprueba from smartmall order By id desc Limit 1', function(err, rows, fields) {
//connection.end();
  //console.log(err);
  if (!err){
    //console.log('The solution is: ', rows);
    console.log(rows[0].luzprueba);
if(rows[0].luzprueba==1)
    {
port.write('h');
}
else
{
port.write('l');
}   

  }
  else
    console.log('Error while performing Query.');
  });

}
