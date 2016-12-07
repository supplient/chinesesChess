

class QueueHourglass(list):
	def top(self):
		if len(self) == 0:
			return None
		else:
			return self[len(self)-1]
			
	def leak(self, old_queue, signal, push_func):
		old_index = self.index(old_queue)
		if old_index == 0:
			return
		new_index = old_index - 1
		push_func(self[new_index], signal)
		
	def pushSignal(self, push_func, signal):
		if (len(self)) == 0:
			raise Exception("No queue in hourglass")
		push_func(self.top(), signal)