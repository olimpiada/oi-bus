package main

import (
	"encoding/json"
	"math/rand"
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
	fmt.Fprintln(w, InternalExcuses[rand.Intn(len(InternalExcuses)))
}

func teapotError(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.WriteHeader(http.StatusTeapot)
	fmt.Fprintln(w, "Odwiedził cię duch niełamania już więcej zasad organizacji zawodów. Nie wysyłaj tej wiadomości do 30 innych zawodników, a nie zostaniesz zdyskwalifikowany.")
}

func WhoIsIt(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_, isParticipant, err := DetectParticipant(r)
	enc := json.NewEncoder(w)
	if err != nil {
		internalError(w, err)
		return
	} else if isParticipant {
		teapotError(w)
		return 
	}

}

// TODO: is this useful
func WhoAmI(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	uid, isParticipant, err := DetectParticipant(r)
	enc := json.NewEncoder(w)
	if err != nil {
		log.Print(err)
		w.WriteHeader(http.InternalServerError)
		enc.Encode(nil)
	} else if isParticipant {
		w.WriteHeader(http.StatusOK)
		enc.Encode(uid)
	} else {
		w.WriteHeader(http.StatusNotFound)
		enc.Encode(nil)
	}
}
