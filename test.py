from __future__ import annotations

class test():
    instance:test = None
    val = None
    def __init__(self, val):
        self.val = val
    
    def setInstance(val):
    
        
        instance = test(val)
        return instance
    
    
a = test.setInstance(2)
print(a.val)