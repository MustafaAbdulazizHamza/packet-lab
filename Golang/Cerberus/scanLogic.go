package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
)

func isValidPorts(s []string) bool {
	for _, i := range s {
		p, err := strconv.Atoi(i)
		if err != nil || !(p > 0 && p <= 65535) {
			return false
		}

	}
	return true
}

func getPortsRange(ports string) []string {
	var pr []string
	if strings.Contains(ports, ",") {
		pr = strings.Split(ports, ",")

	} else if strings.Contains(ports, "-") {
		v := strings.Split(ports, "-")
		if len(v) == 2 && isValidPorts(v) {
			start, _ := strconv.Atoi(v[0])
			end, _ := strconv.Atoi(v[1])
			for i := start; i <= end; i++ {
				pr = append(pr, fmt.Sprint(i))
			}
		}
	} else {
		pr = append(pr, ports)
	}
	if !isValidPorts(pr) {
		fmt.Println("You have entered invalid TCP port(s).")
		os.Exit(1)
	}
	return pr
}

func workers(target string, pandoraScan bool) {
	message := ""
	for port := range ports {
		_, err := net.Dial("tcp", fmt.Sprintf("%s:%d", target, port))
		if err != nil {
			message = ""
		} else {
			if !pandoraScan {
				message = fmt.Sprintf("%d\topen", port)

			} else {
				isPandora := isPandoraServer(target, port)
				if isPandora {
					message = fmt.Sprintf("%d\tOpen\tHTTPs Pandora Server v1", port)
				} else {
					message = fmt.Sprintf("%d\topen", port)
				}

			}
		}
		result <- message
	}
}
func scan(target string, pr []string, pandoraScan bool) {
	defer func() {
		close(ports)
		close(result)
	}()

	for i := 0; i < cap(ports); i++ {
		go workers(target, pandoraScan)
	}
	go func() {
		for _, p := range pr {
			port, _ := strconv.Atoi(p)
			ports <- port
		}
	}()
	portsStatus := make([]string, 0)
	for i := 1; i <= len(pr); i++ {
		r := <-result
		if r != "" {
			portsStatus = append(portsStatus, r)
		}
	}
	fmt.Println("Ports\tStatus")
	for _, ps := range portsStatus {
		fmt.Println(ps)
	}

}
