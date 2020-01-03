package main

import (
	_ "database/sql"
	"flag"
	"log"
	"net/http"
	_ "github.com/mattn/go-sqlite3"
)

var dbfile = flag.String("db", "sqlite db file", "/var/db/oi-seattracker.sqlite3")

func RegisterDevice(w http.ResponseWriter, r *http.Request) {
}

func main() {
	flag.Parse()
	db, err := sql.Open("sqlite3", *dbfile)
	if err != nil {
		log.Fatal(err)
	}
	http.HandleFunc("/api/v1/register", RegisterDevice)
	log.Fatal(http.ListenAndServe(":6401", nil))
}
