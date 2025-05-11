'''
Given an unsorted array of size n. Array elements are in the range of 1 to n. One number from set {1, 2, …n} is missing and one number occurs twice in the array. The task is to find these two numbers.

Examples: 

    Input: arr[] = {3, 1, 3}
    Output: 3, 2
    Explanation: In the array, 2 is missing and 3 occurs twice.

    Input: arr[] = {4, 3, 6, 2, 1, 1}
    Output: 1, 5
    Explanation: 5 is missing and 1 is repeating.
'''

def find_missing_repeating(arr):
    freq = {}
    max_num = -1
    arr_len = len(arr)

    # determine the bounds of the array
    for i in range(arr_len):

        if arr[i] not in freq:
            freq[arr[i]] = 1
        else:
            freq[arr[i]] += 1

        if max_num < arr[i]:
            max_num = arr[i]

    missing_num = None
    duplicate_num = None
    for i in range(1, max_num + 1):
        if i not in freq:
            missing_num = i
        elif freq[i] > 1:
            duplicate_num = i

    return [duplicate_num, missing_num]

'''
Given an array prices[] of length N, representing the prices of the stocks on different days, 
the task is to find the maximum profit possible by buying and selling the stocks on different 
days when at most one transaction is allowed. Here one transaction means 1 buy + 1 Sell.
Note: Stock must be bought before being sold.
'''

def get_maximum_profit(stock_prices: list[int]):

    def max(num1, num2):
        return num1 if num1 >= num2 else num2
    
    def min(num1, num2):
        return num1 if num1 <= num2 else num2
    
    min_price = stock_prices[0]
    max_profit = 0

    for index, price in enumerate(stock_prices):
       min_price = min(min_price, price)
       max_profit = max(max_profit, price - min_price)

    return max_profit

def remove_duplicate_from_sorted_array(sorted_arr: list[int]):
    new_arr = [sorted_arr[0]]
    for i in range(1, len(sorted_arr)):
        if sorted_arr[i] == sorted_arr[i - 1]:
            continue
        else:
            new_arr.append(sorted_arr[i])
    return new_arr

def zig_zag_arr(arr: list[int]):
    def swap(index1, index2):
        temp = arr[index1]
        arr[index1] = arr[index2]
        arr[index2] = temp

    trip = True
    size = len(arr)

    if size <= 1:
        return arr
    
    for i in range(size - 1):
        if trip:
            if arr[i] > arr[i + 1]:
                swap(i, i + 1)
        else:
            if arr[i] < arr[i + 1]:
                swap(i, i + 1)
        trip =  not trip