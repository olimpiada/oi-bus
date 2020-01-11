package main

import (
	"database/sql"
	"fmt"
	"net"
	"sinol3.dasie.mimuw.edu.pl/oi-tech/oi-bus/seattracker"
)

var schema = []string{
	`CREATE TABLE IF NOT EXISTS computers (
		id TEXT UNIQUE,
		mac_address TEXT UNIQUE,
		ip_address TEXT PRIMARY KEY,
	)`,
	`CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY,
		name TEXT,
	)`,
	`CREATE TABLE IF NOT EXISTS mappings (
		uid INTEGER UNIQUE,
		cid TEXT UNIQUE,
	)`,
}

type Computer struct {
	Id string
	Mac net.HardwareAddr
	Ip net.IP
}

type User struct {
	Id int
	Name string
}

type DB struct {
	backend *sql.DB
}

func PrepareDB(backend *sql.DB) (db DB, err error) {
	db.backend = backend
	for _, stmt := range schema {
		_, err = db.backend.Exec(stmt)
		if err != nil {
			return
		}
	}
	return
}

func (d DB) ListComputers() (computers []Computer, err error) {
	var rows *sql.Rows
	rows, err = d.backend.Query("SELECT id, mac_address, ip_address FROM computers")
	if err != nil {
		return
	}
	for rows.Next() {
		var ipS string
		var macS, idS sql.NullString
		err = rows.Scan(&idS, &macS, &ipS)
		if err != nil {
			return
		}

		var ip = net.ParseIP(ipS)
		if ip != nil {
			err = fmt.Errorf("Invalid IP: %v", ipS)
			return
		}
		var mac net.HardwareAddr
		if macS.Valid {
			mac, err = net.ParseMAC(macS.String)
			if err != nil {
				return
			}
		}
		var id string = "<unset>"
		if idS.Valid {
			id = idS.String
		}
		computers = append(computers, Computer { id, mac, ip })
	}
	return computers, rows.Err()
}

func (d DB) AddComputer(computer Computer) (err error) {
	_, err = d.backend.Exec("INSERT INTO computers (id, mac_address, ip_address) VALUES (?, ?, ?) ON CONFLICT (id) DO SET mac_address = COALESCE(mac_address, excluded.mac_address), ip_address = COALESCE(ip_address, excluded.ip_address)", computer.Id, computer.Mac.String(), computer.Ip.String())
	return
}

func (d DB) RemoveComputer(computer Computer) (err error) {
	_, err = d.backend.Exec("DELETE FROM computers WHERE id = ?", computer.Id)
	return
}

func (d DB) AddUser(user User) (err error) {
	_, err = d.backend.Exec("INSERT INTO users (id, name) VALUES (?, ?)", user.Id, user.Name)
	return
}

func (d DB) GetUser(id int) (u User, err error) {
	u.Id = id
	row := d.backend.QueryRow("SELECT name FROM users WHERE id = ?", u.Id)
	err = row.Scan(&u.Name)
	return
}

func (d DB) Who(ip net.IP) (w seattracker.WhoResponse, err error) {
	row := d.backend.QueryRow("SELECT computers.id, computers.ip_address, users.id, users.name FROM computers LEFT OUTER JOIN mappings ON computers.id = mappings.cid LEFT OUTER JOIN users ON mappings.uid = users.id WHERE computers.ip_address = ?", ip.String())
	err = row.Scan(&w.Cid, &w.Ip, &w.Uid, &w.Uname)
	return
}

func (d DB) RemoveUser(user User) (err error) {
	_, err = d.backend.Exec("DELETE FROM users WHERE id = ?", user.Id)
	return
}

func (d DB) AssignUser(user User, computer_id string) (err error) {
	_, err = d.backend.Exec("INSERT INTO mappings (uid, cid) VALUES (?, ?) ON CONFLICT (uid) DO SET cid = excluded.cid", user.Id, computer_id)
	return
}

func (d DB) GetUidOfIp(ip net.IP) (uid int, err error) {
	row := d.backend.QueryRow("SELECT uid FROM mappings INNER JOIN computers ON mappings.cid = computers.id WHERE computers.ip_address = ?", ip.String())
	err = row.Scan(&uid)
	return
}
