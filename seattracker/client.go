package seattracker

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"net/url"
)

type Client struct {
	BaseURL *url.Url
}

const (
	DEFAULT_PORT = 6401
)

func NewLocalClient() Client {
	u, e := url.Parse(fmt.Sprintf("http://%s:%d", "127.0.0.1", DEFAULT_PORT))
	if e != nil {
		panic(e)
	}
	return Client {
		BaseURL: u
	}
}

type Uid int

func mustUrl(u *url.URL, e error) *url.URL {
	if e != nil {
		panic(e)
	}
	return u
}

const whoIsItPath = mustUrl(url.Parse("/whoisit"))

func (c Client) WhoIsIt(ip net.IP) (uid int) {
	u := c.BaseURL.ResolveReference(whoIsItPath)
	params := make(url.Values)
	params.Add("ipaddr", ip.String())
	u.RawQuery = params.Encode()
	r, e := http.Get(u.String())
	if e != nil {
		panic(e)
	}
	defer r.Body.Close()
	if r.StatusCode != http.StatusOK {
		fmt.Errorf("received unexpected response to /whoisit: %d", r.StatusCode)
	}
	dec := json.NewDecoder(r.Body)
	if e = dec.Decode(&uid); e != nil {
		panic(e)
	}
	return
}
