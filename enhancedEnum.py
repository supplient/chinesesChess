from enum import Enum

class EnhancedEnum(Enum):
	@classmethod
	def names(cls):
		return [c.name for c in cls]