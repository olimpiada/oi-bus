package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"
	"mime"
	"net"
	"net/http"
	"path"
	"strings"
)

func IpOfRequest(r *http.Request) (ip net.IP, err error) {
	ipS := strings.SplitN(r.RemoteAddr, ":", 2)
	ip = net.ParseIP(ipS[0])
	if ip == nil {
		err = fmt.Errorf("invalid IP provided by net/http")
	}
	return
}

func DetectParticipant(r *http.Request) (uid int, found bool, err error) {
	var ip net.IP
	ip, err = IpOfRequest(r)
	if err != nil {
		return 0, false, err
	}
	uid, err = db.GetUidOfIp(ip)
	if err == sql.ErrNoRows {
		return 0, false, nil
	}
	if err != nil {
		return 0, false, err
	}
	return uid, true, nil
}

func TeapotParticipants(handlerFunc http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		_, isParticipant, err := DetectParticipant(r)
		if err != nil {
			internalError(w, err)
			return
		}
		if isParticipant {
			teapotError(w)
			return
		}
		handlerFunc(w, r)
	}
}

var teapotContents []byte
var teapotType string

func MakeTea() {
	var err error
	teapotContents, err = ioutil.ReadFile(*Teapot)
	if err != nil {
		log.Panic("failed to read meme file to display to nasty participants")
	}
	teapotType = mime.TypeByExtension(path.Ext(*Teapot))
}

func teapotError(w http.ResponseWriter) {
	w.Header().Set("Content-Type", teapotType)
	w.WriteHeader(http.StatusTeapot)
	w.Write(teapotContents)
}