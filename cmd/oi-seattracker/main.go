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

var db *sql.DB

func main() {
	flag.Parse()
	backend, err := sql.Open("sqlite3", *dbfile)
	if err != nil {
		log.Fatal(err)
	}
	defer backend.Close()
	db, err = PrepareDB(backend)
	if err != nil {
		log.Fatal(err)
	}
	http.HandleFunc("/whoisit", WhoIsIt)
	bind := fmt.Sprintf(":%d", seattracker.DEFAULT_PORT)
	log.Fatal(http.ListenAndServe(bind, nil))
}
