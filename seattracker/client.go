package seattracker

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"net/url"
)

type Client struct {
	BaseURL *url.URL
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
		BaseURL: u,
	}
}

func urlMustParse(rawurl string) *url.URL {
	u, e := url.Parse(rawurl)
	if e != nil {
		panic(e)
	}
	return u
}

const (
	WhoIsItPath = "/whoisit"
	WhoAmIPath = "/whoami"
	HealthcheckPath = "/healthcheck"
)

type WhoResponse struct {
	Cid *string `json:"computer_id"`
	Ip *string `json:"ip_address"`
	Uname *string `json:"user_name"`
	Uid *int `json:"user_id"`
}

var whoIsItSuburl = urlMustParse(WhoIsItPath)
func (c Client) WhoIsIt(ip net.IP) (who WhoResponse) {
	u := c.BaseURL.ResolveReference(whoIsItSuburl)
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
	if e = dec.Decode(&who); e != nil {
		panic(e)
	}
	return
}
