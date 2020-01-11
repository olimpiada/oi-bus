package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net"
	"net/http"
)

var InternalExcuses = []string{
	`o ile zakład że w regionie centralnym działa`,
	`nie mamy pańskiego płaszcza i co nam pan zrobi`,
	`dla bezpieczeństwa zostaną wyłączone wszystkie stacje zawodnicze (tak naprawdę to nie)`,
}

func internalError(w http.ResponseWriter, err error) {
	log.Print(err)
	w.Header().Set("Content-Type", "text/plain")
	w.WriteHeader(http.StatusInternalServerError)
	fmt.Fprintln(w, "Internal server error has occured.")
	fmt.Fprintln(w, InternalExcuses[rand.Intn(len(InternalExcuses))])
}

var WhoIsIt = TeapotParticipants(func(w http.ResponseWriter, r *http.Request) {
	ip := net.ParseIP(r.Header.Get("ipaddr"))
	if ip == nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteStatus(http.StatusBadRequest)
		fmt.Fprintln(w, "?ipaddr= missing or invalid")
		return
	}
	HandleWho(w, ip)
})

func WhoAmI(w http.ResponseWriter, r *http.Request) {
	ip, err := IpOfRequest(r)
	if err != nil {
		internalError(w, err)
		return
	}
	HandleWho(w, ip)
}

func HandleWho(w http.ResponseWriter, ip net.IP) {
	who, err := db.Who(ip)
	if err == sql.ErrNoRows {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	if err != nil {
		internalError(w, err)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	enc := json.NewEncoder(w)
	err = enc.Encode(who)
	if err != nil {
		internalError(w, err)
		return
	}
}

func RegistrationMode(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet, http.MethodHead:
		RegistrationModeGet(w, r)
	case http.MethodPost:
		RegistrationModePost(w, r)
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func Healthcheck(w http.ResponseWriter, r *http.Request) {
	
}


