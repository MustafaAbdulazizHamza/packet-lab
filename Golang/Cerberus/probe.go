package main

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"net/http"
	"time"
)

func isPandoraServer(target string, port int) bool {
	status, err := probeServer(fmt.Sprintf("https://%s:%d/secret", target, port), "", "")
	if err != nil {
		return false
	}
	return status == 401
}

func probeServer(url, username, password string) (int, error) {
	body := []byte(`{"secret-id":"/secretid"}`)
	res, err := sendHTTPRequest("GET", url+"secret", username, password, string(body))
	if err != nil {
		return 0, err
	}
	return res.StatusCode, nil
}
func sendHTTPRequest(method, url, username, password string, body string) (response *http.Response, err error) {
	req, err := http.NewRequest(method, url, bytes.NewBufferString(body))
	if err != nil {
		return nil, err
	}
	req.Header.Set("username", username)
	req.Header.Set("password", password)
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true, // This skips certificate verification
		},
	}

	client := &http.Client{
		Timeout:   time.Second * 10,
		Transport: tr,
	}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	return resp, nil

}
