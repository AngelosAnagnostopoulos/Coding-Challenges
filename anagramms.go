package main

import (
	"fmt"
	"strings"
)

func letterCount(s string) map[string]int {
	words := strings.Split(s, "")
	m := make(map[string]int)
	for _, word := range words {
		m[word]++
	}
	return m
}

func areAnagrams(s1, s2 string) bool {
	if len(s1) != len(s2) {
		return false
	}
	m1 := letterCount(s1)
	m2 := letterCount(s2)

	for key, val := range m1 {
		if v, ok := m2[key]; !ok || val != v {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println(areAnagrams("hiri", "irih"))
	fmt.Println("vim-go")
}
