import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from globalSurgeryCalc import Ui_globalSurgeryCalc

class rkl_globalSurgeryCalc(Ui_globalSurgeryCalc):
	def updateBoth(self):
		self.numDaysTxt = "Total days " + str(self.assumedDt.daysTo(self.relinqDt) + 1)
		self.AssRelTxt = "Assumed care " \
									+ self.assumedDt.toString(self.dt_format) \
									+ "; Relinquished " \
									+ self.relinqDt.toString(self.dt_format)
		self.BothTxt = self.AssRelTxt + "; " + self.numDaysTxt
		self.bothMsgs_lineEdit.setText(self.BothTxt)

	def surgDtChanged(self, new_date):
		self.clearDateRanges()
		self.assumedDt = new_date.addDays(1)
		self.surgeryDt = new_date
		self.globalEndDt = self.surgeryDt.addDays(90)
		self.relinqDt = self.surgeryDt.addDays(90)
		self.rel_dateEdit.setDate(self.relinqDt)
		self.ass_dateEdit.setDate(self.assumedDt)
		self.globalEndDate_dateEdit.setDate(self.globalEndDt)
		self.updateBoth()
		self.updateDateRanges()


	def assDtChanged(self, new_date):
		self.clearDateRanges()
		self.assumedDt = new_date
		self.updateBoth()
		self.updateDateRanges()

	def relDtChanged(self, new_date):
		self.clearDateRanges()
		self.relinqDt = new_date
		self.updateBoth()
		self.updateDateRanges()

	def copySurgDate(self):
		self.clipboard.setText(self.surgeryDt.toString(self.dt_format))
		
	def copyAssDate(self):
		self.clipboard.setText(self.assumedDt.toString(self.dt_format))

	def copyRelDate(self):
		self.clipboard.setText(self.relinqDt.toString(self.dt_format))

	def copyEndGlobalDate(self):
		self.clipboard.setText(self.globalEndDt.toString(self.dt_format))

	def copyBoth(self):
		self.clipboard.setText(self.bothMsgs_lineEdit.text())

	def updateDateRanges(self):
		self.ass_dateEdit.setDateRange(self.assumedDt, self.relinqDt)
		self.rel_dateEdit.setDateRange(self.assumedDt, self.globalEndDt)
		self.ass_dateEdit.userDateChanged.connect(self.assDtChanged)
		self.rel_dateEdit.userDateChanged.connect(self.relDtChanged)
		
	def clearDateRanges(self):
		self.ass_dateEdit.userDateChanged.disconnect(self.assDtChanged)
		self.rel_dateEdit.userDateChanged.disconnect(self.relDtChanged)
		self.ass_dateEdit.clearMinimumDate()
		self.ass_dateEdit.clearMaximumDate()
		self.rel_dateEdit.clearMinimumDate()
		self.rel_dateEdit.clearMaximumDate()

	def __init__(self, globalSurgeryCalc):
		Ui_globalSurgeryCalc.__init__(self)
		self.setupUi(globalSurgeryCalc)
		self.assumedDt = QtCore.QDate.currentDate()
		self.surgeryDt = self.assumedDt.addDays(-1)
		self.globalEndDt = self.surgeryDt.addDays(90)
		self.relinqDt = self.surgeryDt.addDays(90)
		self.dt_format = "MM/dd/yyyy"
		self.ass_dateEdit.setDate(self.assumedDt)
		self.surg_dateEdit.setDate(self.surgeryDt)
		self.rel_dateEdit.setDate(self.relinqDt)
		self.globalEndDate_dateEdit.setDate(self.globalEndDt)
		self.updateBoth()
		self.updateDateRanges()
		self.surg_dateEdit.userDateChanged.connect(self.surgDtChanged)
		self.ass_dateEdit.userDateChanged.connect(self.assDtChanged)
		self.rel_dateEdit.userDateChanged.connect(self.relDtChanged)
		self.copySurgDate_pushButton.clicked.connect(self.copySurgDate)
		self.copyAssDate_pushButton.clicked.connect(self.copyAssDate)
		self.copyRelDate_pushButton.clicked.connect(self.copyRelDate)
		self.copyEndGlobalDate_pushButton.clicked.connect(self.copyEndGlobalDate)
		self.copyBothMsgs_pushButton.clicked.connect(self.copyBoth)
		self.clipboard = QtWidgets.QApplication.clipboard()

if __name__ == '__main__':
	import ctypes
	myappid = u'LoshOptometryLLC.QtGlobalSurgeryCalc.hacks.1' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	app = QtWidgets.QApplication(sys.argv)
	globalSurgeryCalc = QtWidgets.QWidget()

	prog = rkl_globalSurgeryCalc(globalSurgeryCalc)

	globalSurgeryCalc.show()
	sys.exit(app.exec_())