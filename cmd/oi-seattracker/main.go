package main

import (
	"database/sql"
	"flag"
	"fmt"
	"log"
	"net/http"
	_ "github.com/mattn/go-sqlite3"
	"sinol3.dasie.mimuw.edu.pl/oi-tech/oi-bus/seattracker"
)

var DbFile = flag.String("db", "/var/db/oi-seattracker/db.sqlite3", "sqlite db file")
var PwFile = flag.String("pw", "/var/db/oi-seattracker/password.txt", "file into which password will be written on generation")
var RegMode = flag.Bool("regmode", false, "registration mode (everyoneIsAdmin-style)")
var Teapot = flag.String("teapot", "/usr/share/oi-bus/default-meme.jpg", "file to serve to participants trying to access admin interface")

var db DB

func main() {
	flag.Parse()
	MakeTea()
	backend, err := sql.Open("sqlite3", *DbFile)
	if err != nil {
		log.Fatal(err)
	}
	defer backend.Close()
	db, err = PrepareDB(backend)
	if err != nil {
		log.Fatal(err)
	}

	http.HandleFunc(seattracker.WhoIsItPath, WhoIsIt)
	http.HandleFunc(seattracker.WhoAmIPath, WhoAmI)
	http.HandleFunc(seattracker.HealthcheckPath, Healthcheck)
	if *RegMode {
		http.HandleFunc("/", RegistrationMode)
	} else {

	}

	bind := fmt.Sprintf(":%d", seattracker.DEFAULT_PORT)
	log.Fatal(http.ListenAndServe(bind, nil))
}

