package main

import (
	"container/heap"
	"fmt"
	"math"
	"math/rand"
)

type IntHeap []int

func (h IntHeap) Len() int {
	return len(h)
}

func (h IntHeap) Swap(i, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h *IntHeap) Push(x interface{}) {
	*h = append(*h, x.(int))
}

func (h *IntHeap) Peek() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	return x
}

func (h *IntHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func (h IntHeap) Less(i, j int) bool {
	return h[i] < h[j]
}

func createRandArray(size int) []int {
	nums := make([]int, size)

	for i := 0; i < size; i++ {
		nums[i] = rand.Intn(100)
	}

	return nums
}

func heapSort(data *IntHeap, a, b int) {
	first := a
	lo := 0
	hi := b - a

	// Build heap with greatest element at top.
	for i := (hi - 1) / 2; i >= 0; i-- {
		siftDown(data, i, hi, first)
	}

	// Pop elements, largest first, into end of data.
	for i := hi - 1; i >= 0; i-- {
		data.Swap(first, first+i)
		siftDown(data, lo, i, first)
	}
}

func siftDown(data *IntHeap, lo, hi, first int) {
	root := lo
	for {
		child := 2*root + 1
		if child >= hi {
			break
		}
		if child+1 < hi && data.Less(first+child, first+child+1) {
			child++
		}
		if !data.Less(first+root, first+child) {
			return
		}
		data.Swap(first+root, first+child)
		root = child
	}
}

func solution(size int) []float64 {

	medians := make([]float64, size)
	running_count := 0
	running_median := 0.0
	nums := createRandArray(size)
	highers, lowers := &IntHeap{}, &IntHeap{}

	for _, val := range nums {
		addNumber(val, lowers, highers, running_median)
		rebalance(lowers, highers)
		heapSort(lowers, 0, lowers.Len())
		heapSort(highers, 0, highers.Len())
		running_median = getMedian(lowers, highers)
		medians[running_count] = running_median
		running_count += 1
	}

	fmt.Printf("Lowers: %v\nHigher: %v\nResult: ", *lowers, *highers)
	return medians

}

func addNumber(num int, lowers, highers *IntHeap, running_median float64) {

	if lowers.Len() == 0 || running_median > float64(num) {
		heap.Push(lowers, num)
	} else {
		heap.Push(highers, num)
	}

}

func rebalance(lowers, highers *IntHeap) {

	sh := highers.Len()
	sl := lowers.Len()

	big := lowers
	small := highers
	flag := 1
	if sh > sl {
		big = highers
		small = lowers
		flag *= -1
	}
	if math.Abs(float64(sh-sl)) >= 2.0 {
		small.Push(big.Pop().(int) * flag)

	}
}

func getMedian(lowers, highers *IntHeap) float64 {
	if lowers.Len() == 0 && highers.Len() == 0 {
		return 0
	} else if lowers.Len() == highers.Len() {
		return float64(lowers.Peek().(int)+highers.Peek().(int)) / 2.0
	} else if lowers.Len() > highers.Len() {
		return float64(lowers.Peek().(int))
	} else {
		return float64(highers.Peek().(int))
	}
	return 0
}

func main() {
	//rand.Seed(time.Now().Unix())
	res := solution(30)
	fmt.Print(res)
}
