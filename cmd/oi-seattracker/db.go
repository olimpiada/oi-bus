package main

var schema = []string{
	`CREATE TABLE IF NOT EXISTS computers (
		id TEXT PRIMARY KEY,
		mac_address TEXT UNIQUE,
		ip_address TEXT UNIQUE,
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
	Id string,
	Mac net.HardwareAddr,
	Ip net.IP,
}

type User struct {
	Id int,
	Name string,
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
	defer rows.Close()
	for rows.Next() {
		var id, macS, ipS string
		err = rows.Scan(&id, &macS, &ipS)
		if err != nil {
			return
		}
		var mac HardwareAddr
		mac, err = net.ParseMAC(macS)
		if err != nil {
			return
		}
		ip, err = net.ParseIP(ipS)
		if err != nil {
			return
		}
		computers = append(computers, Computer { id, mac, ip })
	}
}

func (d DB) AddComputer(computer Computer) (err error) {
	_, err = d.backend.Exec("INSERT INTO computers (id, mac_address, ip_address) VALUES (%v, %v, %v)", computer.Id, computer.Mac.String(), computer.Ip.String())
	return
}

func (d DB) RemoveComputer(computer Computer) (err error) {
	_, err = d.backend.Exec("DELETE FROM computers WHERE id = %v", computer.Id)
	return
}

func (d DB) AddUser(user User) (err error) {
	_, err = d.backend.Exec("INSERT INTO users (id, name) VALUES (%v, %v)", user.Id, user.Name)
	return
}

func (d DB) RemoveUser(user User) (err error) {
	_, err = d.backend.Exec("DELETE FROM users WHERE id = %v", user.Id)
	return
}

func (d DB) AssignUser(user User) (err error) {
	// TODO
}

func (d DB) GetUidOfIp(ip net.IP) (uid int, err error) {
	row := d.backend.QueryRow("SELECT uid FROM mappings INNER JOIN computers ON mappings.cid = computers.id WHERE computers.ip_address = %v", ip.String)
	err = row.Scan(&uid)
	return
}
