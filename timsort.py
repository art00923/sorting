def timsort(arr, *, key=None, reverse=False):
    """
    In-place Timsort implementation (simplified version without galloping).
    Supports key and reverse parameters.
    """
    if key is None:
        def identity(x): return x
        key = identity

    n = len(arr)

    def calc_minrun(n):
        r = 0
        while n >= 64:
            r |= n & 1
            n >>= 1
        return n + r

    MINRUN = calc_minrun(n)

    def insertion_sort(a, left, right):
        # sort a[left:right] (right exclusive) via insertion sort
        for i in range(left + 1, right):
            temp = a[i]
            j = i - 1
            while j >= left and key(a[j]) > key(temp):
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = temp

    def reverse_range(a, left, right):
        i, j = left, right - 1
        while i < j:
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1

    def merge(a, start, mid, end):
        # merge a[start:mid] and a[mid:end], both sorted
        left = a[start:mid]
        right = a[mid:end]
        i = j = 0
        k = start
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            a[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            a[k] = right[j]
            j += 1
            k += 1

    # Step 1: identify runs and push onto stack
    run_stack = []  # each element: (start, length)

    i = 0
    while i < n:
        run_start = i
        i += 1
        # detect run direction
        if i < n and key(arr[i - 1]) <= key(arr[i]):
            # ascending
            while i < n and key(arr[i - 1]) <= key(arr[i]):
                i += 1
        else:
            # descending
            while i < n and key(arr[i - 1]) > key(arr[i]):
                i += 1
            reverse_range(arr, run_start, i)

        run_len = i - run_start

        # extend to at least MINRUN
        if run_len < MINRUN:
            force = min(MINRUN, n - run_start)
            insertion_sort(arr, run_start, run_start + force)
            run_len = force
            i = run_start + run_len

        run_stack.append([run_start, run_len])

        # merge collapse invariants
        def merge_collapse():
            while True:
                L = len(run_stack)
                if L <= 1:
                    break
                if L >= 3 and run_stack[L - 3][1] <= run_stack[L - 2][1] + run_stack[L - 1][1]:
                    if run_stack[L - 3][1] < run_stack[L - 1][1]:
                        merge_at(L - 3)
                    else:
                        merge_at(L - 2)
                elif L >= 2 and run_stack[L - 2][1] <= run_stack[L - 1][1]:
                    merge_at(L - 2)
                else:
                    break

        def merge_at(idx):
            # merge run_stack[idx] and run_stack[idx+1]
            start, len1 = run_stack[idx]
            _, len2 = run_stack[idx + 1]
            merge(arr, start, start + len1, start + len1 + len2)
            run_stack[idx][1] = len1 + len2
            # remove the next run
            del run_stack[idx + 1]

        merge_at = merge_at  # closure binding
        merge_collapse()

    # Step 2: force merge remaining runs
    while len(run_stack) > 1:
        L = len(run_stack)
        if L >= 3 and run_stack[L - 3][1] < run_stack[L - 1][1]:
            merge_at = lambda idx: None  # placeholder to satisfy structure; will redefine
            # redefine merge_at properly for this scope
            def merge_at(idx):
                start, len1 = run_stack[idx]
                _, len2 = run_stack[idx + 1]
                merge(arr, start, start + len1, start + len1 + len2)
                run_stack[idx][1] = len1 + len2
                del run_stack[idx + 1]
            merge_at(L - 3)
        else:
            # merge last two
            def merge_at_last():
                start, len1 = run_stack[-2]
                _, len2 = run_stack[-1]
                merge(arr, start, start + len1, start + len1 + len2)
                run_stack[-2][1] = len1 + len2
                del run_stack[-1]
            merge_at_last()

    if reverse:
        arr.reverse()
    return arr  # also sorted in-place
