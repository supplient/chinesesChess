#异常类
class UnknownCmdError(Exception):
	pass
class UnknownUserCmdError(UnknownCmdError):
	pass
class UnknownNetCmdError(UnknownCmdError):
	pass
	
class NotLinked(Exception):
	pass