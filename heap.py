class Heap:
    
    def __init__(self, comparison_function, init_array):
        self.comparison_function = comparison_function
        self.heap = init_array
        self.build_heap()
        pass
    
    def build_heap(self):
        
        for i in range(len(self.heap) // 2, -1, -1):
            self._heapify_down(i)
    
    def _heapify_up(self, index):
        
        parent_index = (index - 1) // 2
        if index > 0 and not self.comparison_function(self.heap[parent_index], self.heap[index]):
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        smallest = index

        if left_child < len(self.heap) and not self.comparison_function(self.heap[smallest], self.heap[left_child]):
            smallest = left_child
        if right_child < len(self.heap) and not self.comparison_function(self.heap[smallest], self.heap[right_child]):
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
    
    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
        pass
    
    def extract(self):
        if len(self.heap) == 0:
            return None

        top_value = self.heap[0]
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        self.heap[0] = self.heap.pop()
        if self.heap:
            self._heapify_down(0)
        
        return top_value
        pass
    
    def top(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0]
        pass
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def __str__(self):
        return str(self.heap)
    
    def __repr__(self):
        return self.__str__()