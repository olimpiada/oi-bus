package main

import (
	"net"
	"net/http"
	"strings"
)

func DetectParticipant(r *http.Request) (uid int, found bool, err error) {
	ipS := strings.SplitN(r.RemoteAddr, ":")
	ip := net.ParseIP(ipS)
	var err error
	uid, err = db.GetUidOfIp(ip)
	if err == sql.ErrNoRows {
		return 0, false, nil
	}
	if err != nil {
		return 0, false, err
	}
	return uid, true, nil
}
