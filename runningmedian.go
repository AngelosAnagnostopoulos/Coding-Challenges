package main

import (
	"container/heap"
	"fmt"
	"math"
	"math/rand"
	"time"
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
	x := old[0]
	return x
}

func (h *IntHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[0]
	old[0] = old[n-1]
	*h = old[0 : n-1]
	down(h, 0, n-1)
	return x
}

func down(h *IntHeap, i0, n int) bool {
	i := i0
	for {
		j1 := 2*i + 1
		if j1 >= n || j1 < 0 { // j1 < 0 after int overflow
			break
		}
		j := j1 // left child
		if j2 := j1 + 1; j2 < n && h.Less(j2, j1) {
			j = j2 // = 2*i + 2  // right child
		}
		if !h.Less(j, i) {
			break
		}
		h.Swap(i, j)
		i = j
	}
	return i > i0
}

func (h IntHeap) Less(i, j int) bool {
	return h[i] < h[j]
}

func createRandArray(size int) []int {
	nums := make([]int, size)

	for i := 0; i < size; i++ {
		nums[i] = rand.Intn(10)
	}

	return nums
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
		running_median = getMedian(lowers, highers)
		medians[running_count] = running_median
		running_count += 1
	}

	return medians

}

func addNumber(num int, lowers, highers *IntHeap, running_median float64) {

	if lowers.Len() == 0 || running_median > float64(num) {
		heap.Push(lowers, -num)
	} else {
		heap.Push(highers, num)
	}

}

func rebalance(lowers, highers *IntHeap) {

	sh := highers.Len()
	sl := lowers.Len()

	big := lowers
	small := highers
	flag := -1
	if sh > sl {
		big = highers
		small = lowers
	}
	if math.Abs(float64(sh-sl)) >= 2.0 {
		heap.Push(small, big.Pop().(int)*flag)
	}
}

func getMedian(lowers, highers *IntHeap) float64 {
	if lowers.Len() == 0 && highers.Len() == 0 {
		return 0
	} else if lowers.Len() == highers.Len() {
		return float64(-lowers.Peek().(int)+highers.Peek().(int)) / 2.0
	} else if lowers.Len() > highers.Len() {
		return float64(-lowers.Peek().(int))
	} else {
		return float64(highers.Peek().(int))
	}
	return 0
}

func quickSort(arr []int, low, high int) []int {
	if low < high {
		var p int
		arr, p = partition(arr, low, high)
		arr = quickSort(arr, low, p-1)
		arr = quickSort(arr, p+1, high)
	}
	return arr
}

func partition(arr []int, low, high int) ([]int, int) {
	pivot := arr[high]
	i := low
	for j := low; j < high; j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[high] = arr[high], arr[i]
	return arr, i
}

func naive(size int) []float64 {
	medians := make([]float64, size)
	nums := createRandArray(size)
	for i, _ := range nums {
		quickSort(nums, 0, i)
		medians[i] = float64(nums[i/2]+nums[(i+1)/2]) / 2.0
	}
	return medians
}

func main() {
	rand.Seed(time.Now().Unix())
	res := solution(12)
	rand.Seed(time.Now().Unix())
	res2 := naive(12)

	fmt.Print(res, res2)
}
